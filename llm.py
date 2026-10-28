# llm.py
# ---------------------------------------------------------------------------
# All Groq LLM logic lives here.
# - Builds the prompt for 3 unique project suggestions
# - Calls Groq with high temperature + random seed for variety
# - Validates the JSON response
# - Checks new titles against recent ones and retries if too similar
# ---------------------------------------------------------------------------

import os
import json
import random
import difflib
from collections import deque

import streamlit as st
from groq import Groq

from config import (
    DEFAULT_MODEL,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS,
    TITLE_MEMORY_SIZE,
    TITLES_IN_PROMPT,
    SIMILARITY_THRESHOLD,
    MAX_RETRIES,
)

# ── Creative angles the prompt randomly picks from ──────────────────────────
# Having many angles (15+) ensures variety across students.
CREATIVE_ANGLES = [
    "local-language tool",
    "campus problem solver",
    "small-business helper",
    "health and wellness",
    "sports analytics",
    "agriculture / farming",
    "finance for students",
    "accessibility for differently-abled people",
    "education and learning",
    "entertainment / memes / fun",
    "environment and sustainability",
    "traffic and transport",
    "food and nutrition",
    "career and placement",
    "social media and content creation",
    "disaster preparedness",
    "women's safety",
    "tourism and travel",
    "daily productivity",
    "local news and events",
]

# Output types – each project in a response must use a different one
OUTPUT_TYPES = [
    "chatbot",
    "predictor",
    "summarizer",
    "recommender",
    "classifier",
    "generator",
]

# ── Shared in-memory store for recent project titles ────────────────────────
# st.cache_resource means ONE deque is shared across ALL users in the session,
# so no student gets a title that any recent student also got.

@st.cache_resource
def get_title_memory() -> deque:
    """Return the shared deque that stores recent project titles."""
    return deque(maxlen=TITLE_MEMORY_SIZE)


def _add_titles_to_memory(titles: list[str]) -> None:
    """Add newly generated titles to the shared memory."""
    mem = get_title_memory()
    for t in titles:
        mem.append(t.strip().lower())


def _titles_are_too_similar(new_titles: list[str]) -> bool:
    """
    Return True if any new title is NEARLY IDENTICAL (>= threshold) to any
    title already stored in memory.

    Uses two checks:
    1. Full-string SequenceMatcher ratio (catches rewordings of whole title)
    2. Word-overlap Jaccard index (catches titles that share almost all words)

    Both must be above the threshold to trigger a rejection, preventing
    false positives like "Cricket Predictor" vs "Cricket Chatbot".
    """
    mem = get_title_memory()
    if not mem:
        return False
    for new in new_titles:
        new_lower = new.strip().lower()
        new_words = set(new_lower.split())
        for old in mem:
            old_words = set(old.split())
            # Full-string similarity
            seq_ratio = difflib.SequenceMatcher(
                None, new_lower, old
            ).ratio()
            # Jaccard word overlap (intersection / union)
            if new_words and old_words:
                jaccard = len(new_words & old_words) / len(new_words | old_words)
            else:
                jaccard = 0.0
            # Reject only if BOTH ratios are very high
            if seq_ratio >= SIMILARITY_THRESHOLD and jaccard >= 0.75:
                return True
    return False


def clear_title_memory() -> None:
    """Wipe all stored titles (call this from the UI reset button)."""
    get_title_memory().clear()


def _build_prompt(
    name: str,
    branch: str,
    skills: list[str],
    interests: str,
    experience: str,
    angle: str,
    output_types: list[str],
) -> str:
    """
    Build the system+user prompt that asks the model for exactly 3 projects
    in JSON format.
    """
    mem = get_title_memory()
    # Grab the most recent titles to put in the "avoid" list
    recent = list(mem)[-TITLES_IN_PROMPT:]
    avoid_block = ""
    if recent:
        avoid_block = (
            "\n\nDo NOT suggest anything similar to these recently suggested titles:\n"
            + "\n".join(f"- {t}" for t in recent)
        )

    skills_str = ", ".join(skills) if skills else "None yet"
    types_str  = ", ".join(output_types)

    system_msg = (
        "You are an AI project mentor helping engineering students build their "
        "first AI project in exactly 60 minutes during a hands-on workshop. "
        "Respond ONLY with valid JSON matching the given schema. No markdown, "
        "no explanations outside the JSON."
    )

    user_msg = f"""
Student profile:
- Name: {name}
- Branch: {branch}
- Skills: {skills_str}
- Interests: {interests}
- Experience level: {experience}

Creative angle to inspire you today: "{angle}"
Each project must use a DIFFERENT output type from this list: {types_str}

Suggest exactly 3 AI project ideas that:
1. Directly relate to the student's stated interests and skills.
2. Can be built in 60 minutes by a beginner — use only public APIs or tiny
   pre-trained models (e.g., HuggingFace pipelines). No GPU training.
3. Are meaningfully different from each other in domain AND output type.
4. Feel fresh and personally relevant — not generic "chat with PDF" projects.
{avoid_block}

Respond ONLY with JSON in this exact schema:
{{
  "projects": [
    {{
      "title": "short catchy project name",
      "one_line_pitch": "one sentence that makes the student excited",
      "what_you_will_build_in_60_min": "step-by-step breakdown of the 60 minutes",
      "tools": ["tool or API 1", "tool or API 2"],
      "why_it_fits_you": "1-2 sentences connecting this to the student's interests"
    }}
  ]
}}
"""
    return system_msg, user_msg.strip()


def _validate_response(data: dict) -> bool:
    """
    Check the parsed JSON has exactly 3 projects, each with all required fields.
    Returns True if valid.
    """
    required_fields = {
        "title", "one_line_pitch",
        "what_you_will_build_in_60_min", "tools", "why_it_fits_you"
    }
    projects = data.get("projects", [])
    if len(projects) != 3:
        return False
    for p in projects:
        if not required_fields.issubset(p.keys()):
            return False
        if not isinstance(p.get("tools"), list):
            return False
    return True


def _call_groq(system_msg: str, user_msg: str, model: str) -> dict:
    """
    Make a single call to Groq and return the parsed JSON dict.
    Raises ValueError on bad JSON or failed validation.
    Raises groq.APIError / groq.RateLimitError on API problems.
    """
    # Read the API key from environment (never hardcoded)
    api_key = os.environ.get("GROQ_API_KEY", "")

    # Also check st.secrets (used on Streamlit Community Cloud)
    if not api_key:
        try:
            api_key = st.secrets.get("GROQ_API_KEY", "")
        except Exception:
            pass

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not set. Please add it to your .env file or "
            "Streamlit secrets."
        )

    client = Groq(api_key=api_key)

    # Random seed → different results for same input
    seed = random.randint(0, 2**31 - 1)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user",   "content": user_msg},
        ],
        temperature=LLM_TEMPERATURE,
        max_tokens=LLM_MAX_TOKENS,
        seed=seed,                                  # randomness across runs
        response_format={"type": "json_object"},    # force JSON output
    )

    raw = response.choices[0].message.content
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Model returned invalid JSON: {exc}") from exc

    if not _validate_response(data):
        raise ValueError(
            "Model response did not match expected schema "
            "(need exactly 3 projects with all fields)."
        )

    return data


def generate_projects(
    name: str,
    branch: str,
    skills: list[str],
    interests: str,
    experience: str,
) -> dict:
    """
    Public function called by app.py.

    Returns a validated dict  {"projects": [...]} with 3 unique project ideas.
    Retries up to MAX_RETRIES times if:
      - The JSON is invalid / wrong schema, OR
      - Any new title is too similar to a recently seen title.

    Raises RuntimeError with a user-friendly message if all retries fail.
    """
    model = os.environ.get("GROQ_MODEL", DEFAULT_MODEL)

    last_error = None
    last_good_data = None   # keep the last valid JSON in case all retries fail

    for attempt in range(MAX_RETRIES + 1):
        # Pick a fresh random angle and 3 distinct output types every attempt
        angle = random.choice(CREATIVE_ANGLES)
        output_types = random.sample(OUTPUT_TYPES, 3)

        system_msg, user_msg = _build_prompt(
            name, branch, skills, interests, experience,
            angle, output_types
        )

        try:
            data = _call_groq(system_msg, user_msg, model)
        except ValueError as exc:
            last_error = str(exc)
            continue   # retry with a new angle/seed
        except Exception as exc:
            # Network errors, rate limits, auth errors – don't retry these
            raise RuntimeError(
                f"Could not reach the AI service. Details: {exc}"
            ) from exc

        new_titles = [p["title"] for p in data["projects"]]
        last_good_data = data   # save in case we need the fallback

        # On the very last retry, accept whatever came back rather than
        # showing an error — similarity is a best-effort guard, not a hard rule.
        if attempt == MAX_RETRIES:
            _add_titles_to_memory(new_titles)
            return data

        if _titles_are_too_similar(new_titles):
            last_error = "Generated titles were too similar to recent ones."
            continue   # retry

        # ✅ All good — store titles in memory and return
        _add_titles_to_memory(new_titles)
        return data

    # Should only reach here if every attempt had a ValueError (bad JSON)
    # But if we have any valid data, return it instead of erroring.
    if last_good_data:
        _add_titles_to_memory([p["title"] for p in last_good_data["projects"]])
        return last_good_data

    raise RuntimeError(
        f"The AI returned unexpected responses after {MAX_RETRIES + 1} attempts. "
        f"Last error: {last_error}. Please try again."
    )
