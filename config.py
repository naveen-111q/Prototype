# config.py
# ---------------------------------------------------------------------------
# Central place for all tweakable settings.
# Change these values to match YOUR workshop details.
# ---------------------------------------------------------------------------

# ── Workshop details ────────────────────────────────────────────────────────
WORKSHOP_TITLE = "Build Your First AI Project in 60 Minutes"
WORKSHOP_DATE  = "15 November 2026"          # TODO: update to your actual date

# ── Public URL of this Streamlit app ───────────────────────────────────────
# Used to build the referral share link.
APP_URL = "https://your-app.streamlit.app"   # TODO: update after deployment

# ── Google Form ─────────────────────────────────────────────────────────────
# Paste the URL you get when you click "Get pre-filled link" in Google Forms.
GOOGLE_FORM_URL = (
    "https://docs.google.com/forms/d/e/YOUR_FORM_ID/viewform"
)

# Entry IDs for pre-filled fields.
# HOW TO FIND THEM:
#   1. Open your Google Form.
#   2. Click the three-dot menu → "Get pre-filled link".
#   3. Fill every field with a dummy value, click "Get link".
#   4. Copy the URL. Each field appears as  entry.XXXXXXXXX=dummy_value
#   5. Paste those numbers below (just the digits after "entry.").
FORM_ENTRY_NAME     = "entry.000000001"   # TODO: replace with real entry ID
FORM_ENTRY_BRANCH   = "entry.000000002"   # TODO
FORM_ENTRY_COLLEGE  = "entry.000000003"   # TODO
FORM_ENTRY_EMAIL    = "entry.000000004"   # TODO
FORM_ENTRY_PROJECT  = "entry.000000005"   # TODO: chosen project title
FORM_ENTRY_REF      = "entry.000000006"   # TODO: hidden referral code field
FORM_ENTRY_SRC      = "entry.000000007"   # TODO: hidden source field

# ── Google Sheet (published as CSV) ─────────────────────────────────────────
# HOW TO PUBLISH:
#   1. Open the Google Sheet linked to your form.
#   2. File → Share → Publish to web.
#   3. Choose the correct sheet tab, select "CSV", click Publish.
#   4. Copy the URL and paste it below.
SHEET_CSV_URL = (
    "https://docs.google.com/spreadsheets/d/e/YOUR_SHEET_ID/pub?output=csv"
)

# Column names EXACTLY as they appear in the Sheet header row.
# Adjust these after your form is live and you can see the real column names.
COL_EMAIL    = "Email Address"
COL_NAME     = "Name"
COL_BRANCH   = "Branch"
COL_COLLEGE  = "College"
COL_PROJECT  = "Chosen Project"
COL_REF      = "Referral Code"
COL_SRC      = "Source"
COL_DATE     = "Timestamp"

# ── Referral reward tiers ────────────────────────────────────────────────────
REWARD_TIERS = [
    {"min": 1, "name": "Starter Kit 🎁",       "emoji": "🎁"},
    {"min": 3, "name": "Prompt Pack 📦",        "emoji": "📦"},
    {"min": 5, "name": "Priority Certificate 🏅","emoji": "🏅"},
]

# Registration goal shown on admin dashboard
REGISTRATION_GOAL = 500

# ── LLM settings ─────────────────────────────────────────────────────────────
# Model is also overridable via GROQ_MODEL env variable (see llm.py).
DEFAULT_MODEL = "openai/gpt-oss-120b"
LLM_TEMPERATURE = 1.0          # High temperature → more creative variation
LLM_MAX_TOKENS  = 2048

# Recent-title memory window (in-memory deque, no database)
TITLE_MEMORY_SIZE = 200        # how many past titles to remember
TITLES_IN_PROMPT  = 20         # how many to include in the "avoid" list
SIMILARITY_THRESHOLD = 0.85   # SequenceMatcher ratio above which we regenerate
                                # 0.85 = nearly identical titles only; 0.70 was too aggressive
MAX_RETRIES = 3                # max regeneration attempts before friendly error
