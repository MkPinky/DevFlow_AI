from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_required_project_files_exist():
    required = ["app.py", "agents.py", "tasks.py", "crew.py", "config.py", "requirements.txt", "README.md"]
    for filename in required:
        assert (ROOT / filename).is_file(), f"Missing {filename}"

def test_env_example_does_not_contain_real_key():
    content = (ROOT / ".env.example").read_text(encoding="utf-8")
    assert "your_groq_api_key_here" in content
