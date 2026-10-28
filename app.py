# app.py
# ---------------------------------------------------------------------------
# ProjectMatch – Streamlit frontend (Stage 1 + Stage 2)
# Run with:  streamlit run app.py
# ---------------------------------------------------------------------------

import os
import base64
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# Load .env file when running locally
load_dotenv()

from config import WORKSHOP_TITLE, WORKSHOP_DATE, APP_URL

# ── Page config (must be first Streamlit call) ───────────────────────────────
st.set_page_config(
    page_title="ProjectMatch – Find Your First AI Project",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Helper: embed background image as base64 ────────────────────────────────
def _get_bg_base64() -> str:
    """Read background.jpg and return a base64 data URI."""
    bg_path = Path(__file__).parent / "background.jpg"
    if bg_path.exists():
        with open(bg_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f"data:image/jpeg;base64,{data}"
    return ""

BG_URI = _get_bg_base64()
BG_STYLE = f'background-image: url("{BG_URI}"); background-size: cover; background-attachment: fixed; background-position: center;' if BG_URI else ""

# ── Global CSS (Light Theme) ──────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ---- Page background ---- */
.stApp {{
    {BG_STYLE}
    font-family: 'Inter', sans-serif;
}}

/* Light frosted glass panel */
.stApp > .main > .block-container {{
    background: rgba(255, 255, 255, 0.82);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border-radius: 24px;
    padding: 2rem 2.2rem 3rem;
    margin-top: 1.5rem;
    border: 1px solid rgba(108, 99, 255, 0.12);
    box-shadow: 0 8px 40px rgba(100, 90, 200, 0.10);
}}

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    color: #2d2d4e;
}}

/* ---- Header banner ---- */
.header-banner {{
    background: linear-gradient(135deg, #6C63FF 0%, #43d4d4 100%);
    border-radius: 18px;
    padding: 2rem 1.5rem;
    text-align: center;
    margin-bottom: 1.8rem;
    color: white;
    box-shadow: 0 6px 28px rgba(108,99,255,0.28);
    animation: fadeSlideIn 0.6s ease-out;
}}
.header-banner h1 {{ font-size: 2.2rem; font-weight: 800; margin: 0; letter-spacing: -0.5px; }}
.header-banner p  {{ font-size: 1rem; opacity: 0.92; margin-top: 0.4rem; }}

@keyframes fadeSlideIn {{
    from {{ opacity: 0; transform: translateY(-18px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}

/* ---- Project card (light) ---- */
.project-card {{
    background: linear-gradient(135deg, #ffffff 0%, #f4f3ff 100%);
    border: 1px solid rgba(108, 99, 255, 0.18);
    border-radius: 16px;
    padding: 1.5rem 1.6rem;
    margin-bottom: 1.2rem;
    color: #2d2d4e;
    box-shadow: 0 4px 20px rgba(108,99,255,0.10);
    transition: transform 0.22s ease, box-shadow 0.22s ease;
    animation: cardIn 0.5s ease-out;
}}
.project-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 32px rgba(108,99,255,0.18);
}}
@keyframes cardIn {{
    from {{ opacity: 0; transform: translateY(14px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
.project-card h3 {{ color: #6C63FF; margin-top: 0; font-size: 1.18rem; font-weight: 700; }}
.project-card .pitch {{ font-size: 1.02rem; font-weight: 600; color: #3a3a60; margin: 0.3rem 0 0.8rem; }}
.project-card .section-label {{
    font-size: 0.70rem; text-transform: uppercase;
    letter-spacing: 0.1em; color: #9898bb; margin-top: 1rem; margin-bottom: 0.25rem;
}}
.project-card .tools span {{
    background: rgba(108,99,255,0.10); color: #6C63FF;
    border-radius: 20px; padding: 3px 12px;
    font-size: 0.78rem; margin-right: 6px; display: inline-block;
    margin-top: 4px; border: 1px solid rgba(108,99,255,0.22);
}}

/* ---- Registration / Stage-2 panel ---- */
.reg-panel {{
    background: linear-gradient(135deg, #f8f7ff, #eef6ff);
    border: 1px solid rgba(108,99,255,0.20);
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    margin-top: 1.6rem;
    box-shadow: 0 4px 20px rgba(108,99,255,0.08);
    animation: fadeSlideIn 0.5s ease-out;
}}
.reg-panel h3 {{ color: #6C63FF; font-size: 1.25rem; margin-top: 0; }}

/* ---- Referral code box ---- */
.ref-code-box {{
    background: linear-gradient(135deg, #f0efff, #e8f8f8);
    border: 2px dashed rgba(108,99,255,0.40);
    border-radius: 14px;
    padding: 0.9rem 1.2rem;
    text-align: center;
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: 0.4em;
    color: #6C63FF;
    margin: 0.8rem 0;
}}

/* ---- WhatsApp box ---- */
.wa-box {{
    background: rgba(37,211,102,0.07);
    border: 1px solid rgba(37,211,102,0.30);
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    font-size: 0.88rem;
    color: #1a6e3a;
    white-space: pre-wrap;
    word-break: break-all;
    margin-top: 0.5rem;
}}

/* ---- Buttons ---- */
.stButton > button {{
    background: linear-gradient(135deg, #6C63FF, #43d4d4) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 2rem !important;
    font-weight: 700 !important; font-size: 1rem !important;
    transition: opacity 0.2s, transform 0.15s, box-shadow 0.2s !important;
    width: 100% !important;
    box-shadow: 0 4px 14px rgba(108,99,255,0.25) !important;
}}
.stButton > button:hover {{
    opacity: 0.90 !important; transform: translateY(-2px) !important;
    box-shadow: 0 8px 22px rgba(108,99,255,0.35) !important;
}}

/* ---- Form labels ---- */
label, .stTextInput label, .stSelectbox label,
.stMultiSelect label, .stRadio label {{
    color: #4a4a70 !important; font-weight: 600 !important;
}}

/* ---- Input fields ---- */
.stTextInput input {{
    background: rgba(255,255,255,0.95) !important;
    color: #2d2d4e !important;
    border: 1.5px solid rgba(108,99,255,0.25) !important;
    border-radius: 10px !important;
}}
.stTextInput input:focus {{
    border-color: #6C63FF !important;
    box-shadow: 0 0 0 3px rgba(108,99,255,0.12) !important;
}}

/* ---- Privacy note ---- */
.privacy-note {{
    font-size: 0.78rem; color: #9898bb; text-align: center; margin-top: 0.5rem;
}}

/* ---- Divider ---- */
.styled-divider {{
    border: none; height: 1.5px;
    background: linear-gradient(90deg, transparent, rgba(108,99,255,0.35), transparent);
    margin: 1.8rem 0;
}}

/* ---- Section headings ---- */
.section-title {{
    font-size: 1.35rem; font-weight: 700;
    color: #2d2d4e; margin: 1.2rem 0 0.3rem;
}}
.section-sub {{
    font-size: 0.88rem; color: #7878a0; margin-bottom: 1rem;
}}
</style>
""", unsafe_allow_html=True)

# ── Read URL params (for referral tracking) ───────────────────────────────────
params    = st.query_params
ref_from  = params.get("ref", "")    # who referred this visitor
src_param = params.get("src", "")    # traffic source (e.g. whatsapp, instagram)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="header-banner">
  <h1>🚀 ProjectMatch</h1>
  <p>{WORKSHOP_TITLE} &nbsp;·&nbsp; {WORKSHOP_DATE}</p>
</div>
""", unsafe_allow_html=True)

# ── Stage 1 – Input form ──────────────────────────────────────────────────────
with st.form("student_form"):
    st.markdown('<div class="section-title">🎓 Tell us about yourself</div>', unsafe_allow_html=True)

    name = st.text_input(
        "Your name *",
        placeholder="e.g. Priya Sharma",
    )
    branch = st.selectbox(
        "Branch *",
        ["CSE", "IT", "ECE", "EEE", "Mechanical", "Civil", "Other"],
    )
    skills = st.multiselect(
        "Your skills (pick all that apply) *",
        ["Python", "Java", "C/C++", "Web dev", "Excel", "None yet", "Other"],
        default=["None yet"],
    )
    interests = st.text_input(
        "Your interests *",
        placeholder="e.g. cricket, farming, music, finance",
        help="The more specific, the better your projects will be!",
    )
    experience = st.radio(
        "Experience level *",
        ["Beginner – I'm new to coding", "Some projects – I've built a few things"],
        horizontal=True,
    )

    st.markdown(
        '<p class="privacy-note">🔒 Your free-text inputs are only used to personalise '
        'suggestions and are never stored or logged.</p>',
        unsafe_allow_html=True,
    )
    submitted = st.form_submit_button("✨ Find My Projects", use_container_width=True)

# Small reset helper outside the form (clears stale title memory)
with st.expander("⚠️ Getting repeated suggestions? Click to reset"):
    st.caption(
        "If you see a 'déjà vu' error or keep getting very similar projects, "
        "click below to clear the suggestion memory and start fresh."
    )
    if st.button("🔄 Clear suggestion memory & retry", key="reset_memory"):
        from llm import clear_title_memory
        clear_title_memory()
        # Also clear session state so results disappear
        for k in ["projects", "student", "favourite_idx", "stage2_done",
                  "ref_code", "share_link", "form_url", "wa_msg"]:
            st.session_state.pop(k, None)
        st.success("✅ Memory cleared! Fill in the form above and try again.")
        st.rerun()

# ── Form validation & LLM call ────────────────────────────────────────────────
if submitted:
    errors = []
    if not name.strip():
        errors.append("Please enter your name.")
    if not interests.strip():
        errors.append("Please enter at least one interest.")
    if not skills:
        errors.append("Please select at least one skill option.")

    if errors:
        for e in errors:
            st.error(e)
        st.stop()

    from llm import generate_projects

    with st.spinner("🤖 Thinking of projects just for you…"):
        try:
            result = generate_projects(
                name=name.strip(),
                branch=branch,
                skills=skills,
                interests=interests.strip(),
                experience=experience,
            )
        except RuntimeError as exc:
            st.error(str(exc))
            st.stop()

    st.session_state["projects"]   = result["projects"]
    st.session_state["student"]    = {
        "name":       name.strip(),
        "branch":     branch,
        "skills":     skills,
        "interests":  interests.strip(),
        "experience": experience,
    }
    st.session_state["favourite_idx"] = 0
    st.session_state["stage2_done"]   = False

# ── Display results if projects exist ─────────────────────────────────────────
if "projects" in st.session_state:
    projects = st.session_state["projects"]
    student  = st.session_state["student"]

    st.markdown('<hr class="styled-divider">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-title">🎯 3 Projects Matched for You, '
        f'{student["name"].split()[0]}!</div>'
        f'<div class="section-sub">Personalised to your skills & interests. '
        f'Each can be built in 60 minutes!</div>',
        unsafe_allow_html=True,
    )

    # ── Project cards ─────────────────────────────────────────────────────────
    for idx, proj in enumerate(projects, start=1):
        tools_html = "".join(f'<span>{t}</span>' for t in proj.get("tools", []))
        st.markdown(f"""
<div class="project-card">
  <h3>#{idx} &nbsp;·&nbsp; {proj['title']}</h3>
  <p class="pitch">💡 {proj['one_line_pitch']}</p>

  <div class="section-label">⏱ What you'll build in 60 min</div>
  <p style="margin:0.3rem 0 0.6rem;">{proj['what_you_will_build_in_60_min']}</p>

  <div class="section-label">🔧 Tools you'll use</div>
  <div class="tools" style="margin-top:0.3rem;">{tools_html}</div>

  <div class="section-label">❤️ Why it fits you</div>
  <p style="margin:0.3rem 0 0;">{proj['why_it_fits_you']}</p>
</div>
""", unsafe_allow_html=True)

    # ── Favourite picker ──────────────────────────────────────────────────────
    st.markdown("#### 👆 Pick your favourite project")
    favourite_idx = st.radio(
        "Which project excites you most?",
        options=range(3),
        format_func=lambda i: projects[i]["title"],
        key="favourite_radio",
        index=st.session_state.get("favourite_idx", 0),
    )
    st.session_state["favourite_idx"] = favourite_idx
    chosen_project = projects[favourite_idx]["title"]

    # ════════════════════════════════════════════════════════════════════════
    # ── STAGE 2 – Register + Referral ────────────────────────────────────
    # ════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="styled-divider">', unsafe_allow_html=True)
    st.markdown("""
<div class="reg-panel">
  <h3>📝 Step 2 — Register for the Workshop</h3>
  <p style="color:#aab0cc;font-size:0.92rem;margin-top:-0.4rem;">
    Enter your email to get your personal referral link, then click
    <strong>Register</strong> to open the Google Form (pre-filled!).
  </p>
</div>
""", unsafe_allow_html=True)

    # Email input (outside the form so it's interactive without re-running LLM)
    email_input = st.text_input(
        "Your college email address *",
        placeholder="yourname@college.edu",
        key="email_input",
    )

    college_input = st.text_input(
        "College name *",
        placeholder="e.g. JNTU Hyderabad",
        key="college_input",
    )

    reg_clicked = st.button("📋 Register for the Workshop", use_container_width=True, key="reg_btn")

    if reg_clicked:
        if not email_input.strip():
            st.error("Please enter your email address to continue.")
        elif "@" not in email_input or "." not in email_input.split("@")[-1]:
            st.error("Please enter a valid email address.")
        elif not college_input.strip():
            st.error("Please enter your college name.")
        else:
            from referral import (
                generate_referral_code, build_share_link,
                build_google_form_url, build_whatsapp_message,
            )

            # Generate deterministic referral code from email
            ref_code   = generate_referral_code(email_input.strip())
            share_link = build_share_link(ref_code)

            # Build pre-filled Google Form URL
            form_url = build_google_form_url(
                name           = student["name"],
                branch         = student["branch"],
                email          = email_input.strip(),
                chosen_project = chosen_project,
                ref_code       = ref_from or "",   # who referred THIS student
                src            = src_param or "direct",
            )

            # WhatsApp share message
            wa_msg = build_whatsapp_message(student["name"].split()[0], share_link)

            # Store in session so it persists across reruns
            st.session_state["ref_code"]   = ref_code
            st.session_state["share_link"] = share_link
            st.session_state["form_url"]   = form_url
            st.session_state["wa_msg"]     = wa_msg
            st.session_state["stage2_done"] = True

    # ── Show referral card once details are set ───────────────────────────────
    if st.session_state.get("stage2_done"):
        ref_code   = st.session_state["ref_code"]
        share_link = st.session_state["share_link"]
        form_url   = st.session_state["form_url"]
        wa_msg     = st.session_state["wa_msg"]

        st.success(f"✅ Great, {student['name'].split()[0]}! Here's everything you need:")

        # Open Google Form in new tab
        st.markdown(
            f"""<a href="{form_url}" target="_blank" style="
                display:block; text-align:center; margin:0.8rem 0;
                background: linear-gradient(135deg,#6C63FF,#43d4d4);
                color:white; font-weight:700; font-size:1.05rem;
                padding:0.75rem 1rem; border-radius:12px;
                text-decoration:none; box-shadow:0 4px 18px rgba(108,99,255,0.28);
                transition: opacity 0.2s;
            ">🔗 Open Registration Form (Google Form)</a>""",
            unsafe_allow_html=True,
        )
        st.caption(
            "The form opens in a new tab with your details pre-filled. "
            "Just hit Submit!"
        )

        st.markdown('<hr class="styled-divider">', unsafe_allow_html=True)

        # ── Referral code ──────────────────────────────────────────────────
        st.markdown("#### 🎁 Your Personal Referral Code")
        st.markdown(
            f'<div class="ref-code-box">{ref_code}</div>',
            unsafe_allow_html=True,
        )
        st.caption(
            f"Share your link and earn rewards when friends register:\n\n"
            f"**{share_link}**"
        )

        # Copy-able share link
        st.code(share_link, language=None)

        # ── WhatsApp message ───────────────────────────────────────────────
        st.markdown("#### 📲 Ready-to-send WhatsApp Message")
        st.markdown(
            f'<div class="wa-box">{wa_msg}</div>',
            unsafe_allow_html=True,
        )
        st.code(wa_msg, language=None)

        # ── Reward tiers preview ───────────────────────────────────────────
        st.markdown("#### 🏆 Referral Rewards")
        cols = st.columns(3)
        tiers = [
            ("1 referral",  "🎁 Starter Kit"),
            ("3 referrals", "📦 Prompt Pack"),
            ("5 referrals", "🏅 Priority Certificate"),
        ]
        for col, (req, reward) in zip(cols, tiers):
            with col:
                st.markdown(f"""
<div style="background:linear-gradient(135deg,#f4f3ff,#eef8ff);border:1px solid rgba(108,99,255,0.18);
border-radius:12px;padding:0.8rem;text-align:center;box-shadow:0 2px 10px rgba(108,99,255,0.08);">
  <div style="font-size:1.4rem;">{reward.split()[0]}</div>
  <div style="font-size:0.80rem;color:#6C63FF;font-weight:700;margin-top:0.2rem;">{reward.split(' ',1)[1]}</div>
  <div style="font-size:0.70rem;color:#9898bb;margin-top:0.2rem;">{req}</div>
</div>
""", unsafe_allow_html=True)

        st.markdown(
            '<p class="privacy-note" style="margin-top:1rem;">Check your rewards anytime on the '
            '"My Rewards" page (coming soon).</p>',
            unsafe_allow_html=True,
        )
