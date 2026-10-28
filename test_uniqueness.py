# test_uniqueness.py
# ---------------------------------------------------------------------------
# Quick test: submit the SAME inputs 5 times and print all 15 project titles.
# This proves that identical inputs produce different suggestions each run.
#
# Usage (from the project folder, with GROQ_API_KEY set):
#   python test_uniqueness.py
# ---------------------------------------------------------------------------

# Force UTF-8 output on Windows terminals
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os
import textwrap
from dotenv import load_dotenv

load_dotenv()  # loads .env so GROQ_API_KEY is available

# We need to mock streamlit's cache_resource since we're running outside Streamlit
# Patch it before importing llm.py
import unittest.mock as mock

# Create a real deque that the mock returns (shared across calls)
from collections import deque
_shared_memory = deque(maxlen=200)

# Patch st.cache_resource so get_title_memory() just returns our deque
import streamlit as st
with mock.patch.object(st, 'cache_resource', lambda fn: lambda: _shared_memory):
    # Also patch st.secrets to avoid StreamlitSecretNotFoundError
    with mock.patch.object(st, 'secrets', {}, create=True):
        import llm
        # Override get_title_memory to return our shared deque
        llm.get_title_memory = lambda: _shared_memory

        # ── Fixed test inputs ──────────────────────────────────────────────
        TEST_NAME       = "Ravi Kumar"
        TEST_BRANCH     = "CSE"
        TEST_SKILLS     = ["Python"]
        TEST_INTERESTS  = "cricket, farming, music"
        TEST_EXPERIENCE = "Beginner – I'm new to coding"

        print("=" * 65)
        print("ProjectMatch – Uniqueness Test")
        print(f"Input: {TEST_NAME} | {TEST_BRANCH} | {TEST_SKILLS}")
        print(f"       Interests: {TEST_INTERESTS}")
        print("=" * 65)

        all_titles = []

        for run in range(1, 6):
            print(f"\n-- Run {run} " + "-"*50)
            try:
                result = llm.generate_projects(
                    name=TEST_NAME,
                    branch=TEST_BRANCH,
                    skills=TEST_SKILLS,
                    interests=TEST_INTERESTS,
                    experience=TEST_EXPERIENCE,
                )
                titles = [p["title"] for p in result["projects"]]
                all_titles.extend(titles)
                for i, (title, proj) in enumerate(
                    zip(titles, result["projects"]), 1
                ):
                    print(f"  {i}. {title}")
                    print(f"     Tools: {', '.join(proj['tools'])}")
                    wrapped = textwrap.fill(
                        proj["one_line_pitch"], width=60,
                        initial_indent="     Pitch: ",
                        subsequent_indent="            "
                    )
                    print(wrapped)
            except RuntimeError as exc:
                print(f"  ERROR: {exc}")

        print("\n" + "=" * 65)
        print("All 15 titles across 5 runs:")
        for i, t in enumerate(all_titles, 1):
            print(f"  {i:2d}. {t}")

        # Check for exact duplicates
        unique = set(t.lower() for t in all_titles)
        print(f"\nUnique titles: {len(unique)} / {len(all_titles)}")
        if len(unique) == len(all_titles):
            print("✅ PASS – All titles are unique across 5 runs!")
        else:
            print("⚠️  Some titles were repeated (this can happen with "
                  "very similar inputs; check similarity threshold).")
        print("=" * 65)
