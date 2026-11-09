
import os
from pathlib import Path
from crewai import LLM
# Workaround for CrewAI cache_breakpoint issue with Groq
import crewai.llms.cache as _crewai_cache

_crewai_cache.mark_cache_breakpoint = lambda msg: msg

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"

def ensure_output_dirs():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def get_llm():
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not configured. Add it to your .env file.")
    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b").strip()
    # CrewAI's LLM wrapper uses LiteLLM. The groq/ prefix selects Groq as provider.
    return LLM(
        model=f"groq/{model}",
        api_key=api_key,
        temperature=0.2
    )
