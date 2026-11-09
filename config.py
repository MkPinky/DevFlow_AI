
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from crewai import LLM

# Load local .env variables when running on your computer
load_dotenv()

# Workaround for CrewAI cache_breakpoint issue with Groq
import crewai.llms.cache as _crewai_cache

_crewai_cache.mark_cache_breakpoint = lambda msg: msg

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"


def get_setting(name, default=""):
    """Read Streamlit Secrets first, then fall back to environment variables."""
    try:
        value = st.secrets.get(name)
    except Exception:
        value = None

    return str(value or os.getenv(name, default)).strip()


def ensure_output_dirs():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def get_llm():
    api_key = get_setting("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Add it to your local .env file "
            "or configure it in Streamlit Cloud Secrets."
        )

    model = get_setting("GROQ_MODEL", "openai/gpt-oss-20b")

    return LLM(
        model=f"groq/{model}",
        api_key=api_key,
        temperature=0.2
    )
