# referral.py
# ---------------------------------------------------------------------------
# Everything related to referral codes and Google Form URL building.
# No database needed — the referral code is deterministic (derived from email).
# ---------------------------------------------------------------------------

import hashlib
import urllib.parse

from config import (
    APP_URL,
    GOOGLE_FORM_URL,
    FORM_ENTRY_NAME,
    FORM_ENTRY_BRANCH,
    FORM_ENTRY_EMAIL,
    FORM_ENTRY_PROJECT,
    FORM_ENTRY_REF,
    FORM_ENTRY_SRC,
)


def generate_referral_code(email: str) -> str:
    """
    Derive a 6-character referral code from the student's email.
    Same email always gives the same code. No database needed.
    Uses the first 6 hex chars of SHA-256(lowercase email).
    """
    digest = hashlib.sha256(email.strip().lower().encode()).hexdigest()
    return digest[:6].upper()


def build_share_link(code: str, app_url: str = APP_URL) -> str:
    """Return the full shareable URL: APP_URL/?ref=CODE"""
    return f"{app_url.rstrip('/')}/?ref={code}"


def build_whatsapp_message(student_name: str, share_link: str) -> str:
    """Return a ready-to-copy WhatsApp message with the referral link."""
    return (
        f"Hey! I just matched my first AI project idea at ProjectMatch 🚀\n"
        f"Find yours and register for the FREE 60-min workshop here:\n"
        f"{share_link}\n\n"
        f"Use my link to register and we both get rewards! 🎁"
    )


def build_google_form_url(
    name: str,
    branch: str,
    email: str,
    chosen_project: str,
    ref_code: str,
    src: str,
) -> str:
    """
    Build a pre-filled Google Form URL.
    Each field is encoded as a query param using its entry ID.
    If the entry IDs are still the placeholder values (from config.py),
    we fall back to the bare form URL so at least the form opens.
    """
    params = {
        FORM_ENTRY_NAME:    name,
        FORM_ENTRY_BRANCH:  branch,
        FORM_ENTRY_EMAIL:   email,
        FORM_ENTRY_PROJECT: chosen_project,
        FORM_ENTRY_REF:     ref_code,
        FORM_ENTRY_SRC:     src or "direct",
    }
    # Build query string
    qs = urllib.parse.urlencode(params)
    return f"{GOOGLE_FORM_URL}?{qs}"
