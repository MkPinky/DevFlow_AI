from crewai import Agent
from config import get_llm

def create_agents():
    llm = get_llm()
    requirements_agent = Agent(
        role="Software Requirements Analyst",
        goal="Translate the user's software idea into clear, testable functional and non-functional requirements.",
        backstory="You are a meticulous business analyst who clarifies scope, users, assumptions and acceptance criteria.",
        llm=llm, verbose=True, allow_delegation=False
    )
    architect_agent = Agent(
        role="Software Solution Architect",
        goal="Design a practical architecture, modules, data model and technology choices that fit the requirements.",
        backstory="You are an experienced solution architect who favors understandable, maintainable prototype designs.",
        llm=llm, verbose=True, allow_delegation=False
    )
    code_agent = Agent(
        role="Prototype Code Generator",
        goal="Propose a small, coherent prototype implementation with file names and readable code.",
        backstory="You are a senior developer. You generate reviewable code, avoid destructive operations and never claim untested code works.",
        llm=llm, verbose=True, allow_delegation=False
    )
    testing_agent = Agent(
        role="Software Test Analyst",
        goal="Create test scenarios, expected results, edge cases and a safe manual test procedure for the proposed prototype.",
        backstory="You are a quality engineer. You review the requirements and proposed code, and distinguish proposed tests from executed tests.",
        llm=llm, verbose=True, allow_delegation=False
    )
    documentation_agent = Agent(
        role="Technical Documentation Specialist",
        goal="Write installation, configuration, usage and maintenance documentation consistent with the proposed design.",
        backstory="You are a technical writer who produces precise instructions and clearly marks assumptions.",
        llm=llm, verbose=True, allow_delegation=False
    )
    report_agent = Agent(
        role="Project Report Specialist",
        goal="Prepare a concise final project report summarizing the development outputs, decisions, tests and limitations.",
        backstory="You are a project analyst who reports only what the previous agents produced and never invents execution evidence.",
        llm=llm, verbose=True, allow_delegation=False
    )
    return [requirements_agent, architect_agent, code_agent, testing_agent, documentation_agent, report_agent]
