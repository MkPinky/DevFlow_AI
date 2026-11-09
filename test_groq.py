
import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

if not api_key:
    raise ValueError("Groq API key not found in .env")

llm = LLM(
    model=f"groq/{model}",
    api_key=api_key,
    temperature=0.2
)

response = llm.call(
    messages=[
        {
            "role": "user",
            "content": "Reply with: DevFlow AI Groq connection successful."
        }
    ]
)

print(response)
