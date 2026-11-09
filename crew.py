from crewai import Crew, Process

from agents import create_agents
from tasks import create_tasks


def run_development_crew(project):
    """
    Run the six-agent sequential DevFlow AI workflow.

    Each task has deliberately limited context in tasks.py to reduce
    repeated prompt tokens and lower the chance of Groq TPM errors.
    """
    agents = create_agents()
    tasks = create_tasks(agents)

    crew = Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
        memory=False,
        planning=False,
    )

    result = crew.kickoff(inputs=project)

    # Keep the existing output contract expected by app.py.
    task_outputs = getattr(result, "tasks_output", []) or []
    output_keys = [
        "requirements",
        "architecture",
        "code",
        "testing",
        "documentation",
        "report",
    ]

    outputs = {}
    for index, key in enumerate(output_keys):
        if index < len(task_outputs):
            task_output = task_outputs[index]
            outputs[key] = str(getattr(task_output, "raw", task_output))
        else:
            outputs[key] = ""

    return outputs
