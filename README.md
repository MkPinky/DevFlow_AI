# DevFlow AI
**AI-Powered Multi-Agent Project Development Assistant**

DevFlow AI is a functional prototype that uses six specialist CrewAI agents to turn a software idea into a development blueprint:
1. Requirements analysis
2. Solution architecture
3. Prototype code proposal
4. Test planning and code review
5. Technical documentation
6. Final project report

## Technology
- Python 3.11
- Streamlit
- CrewAI
- Groq API through LiteLLM
- Model: `openai/gpt-oss-20b` (configurable)

## Setup on Windows / PyCharm

1. Open this project folder in PyCharm.
2. Open the PyCharm terminal.
3. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use this command in the same terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

4. Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

5. Create a `.env` file by copying `.env.example`. Add your own Groq API key:

```env
GROQ_API_KEY=your_actual_key
GROQ_MODEL=openai/gpt-oss-20b
```

Never commit `.env` or share the key in screenshots, videos or public repositories.

6. Start the application:

```powershell
streamlit run app.py
```

## How to use
- Enter a project title and description.
- Select language, database and project type.
- Enter required features, one per line.
- Click **Generate Development Plan**.
- Review each agent's output and download the combined Markdown plan.

## Example demonstration input
**Title:** AS Academy Management System

**Description:** A web application to help a coaching centre manage administrators, teachers, students, classes, subjects and academic progress.

**Users:** Admin, teachers and students.

**Features:**
- Admin login
- Teacher registration and login
- Assign classes and subjects to teachers
- Maintain student records
- Track chapter completion and progress

This is only a demonstration idea. DevFlow AI can accept other software ideas too.

## Safety and limitations
- The application generates proposals; it does not autonomously modify your computer.
- Generated code is not executed automatically.
- The testing agent creates proposed test cases; it does not claim tests passed without execution evidence.
- Review all generated code before running it. Use synthetic data and an isolated environment for testing.
- AI-generated requirements, architecture and code require human review.
- API usage is subject to Groq account limits and pricing.

## Project structure

```text
DevFlow_AI/
├── app.py
├── agents.py
├── tasks.py
├── crew.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
├── outputs/
└── README.md
```
