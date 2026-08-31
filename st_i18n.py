"""Bilingual helper for the Streamlit apps (en / ru).

Language choice, highest priority first:
  1. ?lang=ru | ?lang=en    explicit link, and what the sidebar picker writes
  2. st.session_state       the visitor's choice earlier in this session
  3. Accept-Language        sent by the browser; the server-side counterpart of
                            navigator.language used by the static pages
  4. 'en'
"""
import streamlit as st

LANGS = ("en", "ru")
LABELS = {"en": "EN", "ru": "RU"}


def _from_accept_language():
    try:
        header = st.context.headers.get("Accept-Language", "") or ""
    except Exception:
        return None
    for part in header.split(","):
        tag = part.split(";")[0].strip().lower()
        if tag.startswith("ru"):
            return "ru"
        if tag.startswith("en"):
            return "en"
    return None


def resolve_lang():
    """Current language, seeding session state on first run."""
    requested = st.query_params.get("lang")
    if requested in LANGS:
        st.session_state["lang"] = requested
    elif "lang" not in st.session_state:
        st.session_state["lang"] = _from_accept_language() or "en"
    return st.session_state["lang"]


def language_picker(lang):
    """Sidebar EN/RU switch. Returns the (possibly new) language."""
    choice = st.sidebar.radio(
        "Language / Язык",
        LANGS,
        index=LANGS.index(lang),
        format_func=lambda code: LABELS[code],
        horizontal=True,
        key="_lang_picker",
    )
    if choice != lang:
        st.session_state["lang"] = choice
        st.query_params["lang"] = choice
        st.rerun()
    return choice


def translator(strings, lang):
    """t('key') -> string in `lang`, falling back to the key itself."""
    def t(key):
        entry = strings.get(key)
        if entry is None:
            return key
        return entry.get(lang, entry.get("en", key))
    return t
