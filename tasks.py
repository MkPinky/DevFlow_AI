from crewai import Task


def create_tasks(agents):
    """
    Build the six-task sequential DevFlow AI workflow.

    The workflow creates a traceable chain:
    Requirements -> Architecture -> Code -> Testing -> Documentation -> Report.

    Important:
    - Generated code and proposed tests are not considered executed evidence.
    - Each downstream task must inspect the actual upstream deliverables.
    - Acceptance criteria must be assessed individually.
    """
    if len(agents) != 6:
        raise ValueError(
            "create_tasks() requires exactly 6 agents in this order: "
            "requirements, architect, coder, tester, documenter, reporter."
        )

    requirements, architect, coder, tester, documenter, reporter = agents

    # 1. Requirements Analyst
    task1 = Task(
        description="""
Create a clear, testable requirements specification from the project brief.

PROJECT BRIEF
Title: {title}
Description: {description}
Intended users: {audience}
Required features: {features}
Language: {language}
Database: {database}
Project type: {project_type}
Complexity: {complexity}
Constraints: {constraints}

Required sections:
1. Problem statement
2. User roles and permissions
3. Functional requirements with unique IDs: FR-01, FR-02, ...
4. Non-functional requirements with unique IDs: NFR-01, NFR-02, ...
5. Scope and exclusions
6. Assumptions and open questions
7. Acceptance criteria with unique IDs: AC-01, AC-02, ...
8. A traceability note mapping every AC to one or more FR/NFR IDs.

Quality rules:
- Treat only the supplied brief as confirmed user requirements.
- Do not invent features, users, business rules, or implementation status.
- Label assumptions and recommendations separately.
- Make acceptance criteria observable and testable.
- Ensure every acceptance criterion maps to an existing requirement ID.
- Do not claim that any feature has already been implemented.
- Keep requirement IDs stable for all later agents.

Use concise headings and tables where useful. Prefer completeness and clarity over an arbitrary word limit.
""",
        expected_output=(
            "A requirements specification containing problem statement, roles, "
            "FR/NFR IDs, scope, assumptions, open questions, measurable ACs, "
            "and an FR/NFR-to-AC traceability mapping."
        ),
        agent=requirements,
    )

    # 2. Solution Architect
    task2 = Task(
        description="""
Design a practical architecture using the Requirements task as the source of truth.

PROJECT
Title: {title}
Language: {language}
Database: {database}
Project type: {project_type}
Complexity: {complexity}
Constraints: {constraints}

Required sections:
1. Architecture overview and major layers
2. Modules/components and their responsibilities
3. User workflows for each role
4. Data model: entities/collections, important fields, and relationships
5. API/service boundaries or data access responsibilities, where relevant
6. FR-to-module mapping for EVERY FR ID
7. NFR-to-design-control mapping for EVERY NFR ID
8. Authentication, authorization, validation, and data security design
9. Mermaid architecture diagram
10. Design assumptions and unresolved decisions

Quality rules:
- Map every FR ID. If a requirement is not designed, explicitly say "Not designed" and explain why.
- Map every NFR ID to a proposed design measure or mark it "Not addressed".
- Distinguish proposed components from components that already exist. No implementation is assumed.
- For Firebase projects, distinguish Firebase Authentication from Firestore Security Rules. UI role checks alone are not security enforcement.
- Do not claim security rules, APIs, screens, or services exist unless supplied evidence shows they exist.
- Avoid adding technologies that are not justified by the brief.
- Keep naming consistent with the requirements.

Produce a sufficiently detailed design that the Code Generation Agent can implement one selected feature without guessing.
""",
        expected_output=(
            "Architecture overview, component responsibilities, data model, "
            "role workflows, complete FR/NFR mapping, security design, "
            "assumptions, and a valid Mermaid diagram."
        ),
        agent=architect,
        context=[task1],
    )

    # 3. Code Generation Specialist
    task3 = Task(
        description="""
Generate a small but COMPLETE prototype for one clearly selected core feature.

PROJECT
Title: {title}
Language: {language}
Database: {database}
Project type: {project_type}
Constraints: {constraints}

Use the Requirements and Architecture tasks as the source of truth.

Before writing code:
- Select one core feature that can realistically be delivered as a working prototype.
- State the FR IDs the prototype is intended to cover.
- State any related FR/NFR IDs that remain outside the prototype.

Required output:
1. Prototype scope and selected feature
2. Exact folder/file tree
3. Dependency list and configuration prerequisites
4. Complete contents of EVERY file in the tree
5. Setup and run commands
6. Manual steps needed for external services, such as Firebase configuration
7. Known limitations and omitted functionality
8. A file-to-purpose table and FR coverage statement

Code quality rules:
- All referenced imports and project files must be included or explicitly identified as external prerequisites.
- Include an actual application entry point when the output is an application.
- Do not list a file in the tree without providing its contents, unless it is clearly labelled as a pre-existing/generated platform file.
- Do not provide truncated files, pseudocode, ellipses, "rest of code here", or unexplained placeholders in code that is claimed to be complete.
- Keep function, class, collection, and field names consistent across files.
- Include input validation, loading states, and user-friendly error handling where relevant.
- Do not claim that code was executed, compiled, or tested. State "Not executed" unless execution evidence is supplied.
- Never include real API keys, passwords, tokens, or other secrets.
- Never use eval(), exec(), shell=True, destructive commands, or unsafe execution shortcuts.
- If a complete prototype cannot fit in the response, reduce the feature scope rather than omitting required files.
- Prefer one genuinely coherent feature over a broad collection of incomplete screens.

Do not claim that the whole project is implemented. Clearly distinguish prototype code from the proposed full system.
""",
        expected_output=(
            "A complete, internally consistent prototype with a file tree, "
            "full file contents, dependencies, setup/run instructions, "
            "FR coverage statement, and explicit execution status."
        ),
        agent=coder,
        context=[task1, task2],
    )

    # 4. Testing and Code Review Specialist
    task4 = Task(
        description="""
Inspect the actual Requirements, Architecture, and Code Generation outputs.
Create a code-aware test plan and coverage review. Do not assess features based only on the requirements or architecture.

Required output:
A. Exactly five proposed test cases. For each include:
- Test ID (TC-01 to TC-05)
- Related FR/AC ID(s)
- Preconditions
- Test steps
- Expected result
- Evidence location (file/function/screen, if present)
- Coverage status: Implemented in supplied code / Partially implemented / Not implemented

B. Code inspection:
- List up to five concrete defects or omissions.
- Refer to the actual file, class, function, or missing file where possible.
- Identify incomplete code, missing entry points, unresolved imports, inconsistent names, and missing error handling.

C. Security review:
- List up to three concrete security risks tied to the supplied design or code.
- Distinguish a confirmed issue from a risk that requires runtime/configuration verification.

D. Coverage summary:
- List every FR ID not implemented by the supplied prototype.
- Identify acceptance criteria that cannot be met by the supplied code.

Strict rules:
- A proposed test is NOT an executed test.
- Do not use PASS, FAIL, or "tested successfully" unless actual execution logs/results are supplied.
- Mark a requirement as implemented only when corresponding code is actually present and sufficiently complete.
- A file name or architecture diagram is not implementation evidence.
- If code is truncated, missing, or references an absent file, mark the affected feature as partially implemented or not implemented.
- Do not mark a test "covered" merely because a function name or screen is mentioned.
- Check whether navigation, application entry point, configuration, and supporting files actually exist.
- Do not invent test evidence.

Keep the review concise but specific. Accuracy is more important than a positive assessment.
""",
        expected_output=(
            "Exactly five traceable proposed test cases, evidence-based coverage "
            "statuses, code defects, security risks, and a list of unmet FR/AC IDs."
        ),
        agent=tester,
        context=[task1, task2, task3],
    )

    # 5. Documentation Specialist
    task5 = Task(
        description="""
Write README-style documentation for the prototype that was ACTUALLY supplied by the Code Generation Agent.

PROJECT
Title: {title}
Language: {language}
Database: {database}

Use the Requirements, Architecture, Code, and Testing outputs. The code output is the source of truth for files and implemented behaviour.

Required sections:
1. Project overview and prototype scope
2. Implemented feature(s), with related FR IDs
3. Features not implemented
4. Prerequisites
5. Dependencies
6. Configuration steps
7. Exact folder/file structure
8. Installation and run commands
9. How to use the implemented feature
10. Known limitations and troubleshooting

Accuracy rules:
- Verify every documented filename against the Code Generation output.
- Do not document a file that was not supplied, except an external prerequisite clearly labelled as such.
- Do not invent package versions, commands, repository URLs, environment variables, credentials, or configuration files.
- If a required file is missing, explicitly report that the project is incomplete instead of inventing its contents.
- Distinguish "implemented in supplied code" from "planned/proposed".
- Do not claim the app was run, built, or tested.
- Keep instructions appropriate for the specified language and project type.
- Ensure documented commands agree with the supplied project structure.

The README must help a beginner understand what is genuinely present and what remains to be done.
""",
        expected_output=(
            "An accurate README matching the supplied files, dependencies, "
            "configuration, commands, implemented scope, and limitations."
        ),
        agent=documenter,
        context=[task1, task2, task3, task4],
    )

    # 6. Project Report and Consistency Reviewer
    task6 = Task(
        description="""
Prepare the final academic project report and perform a strict cross-agent consistency audit.

PROJECT
Title: {title}
Description: {description}
Language: {language}
Database: {database}
Project type: {project_type}
Intended users: {audience}
Constraints: {constraints}

Review ALL preceding outputs: Requirements, Architecture, Code, Testing, and Documentation.

Use these headings:
1. Abstract
2. Introduction and Problem Statement
3. Objectives
4. Requirements Summary
5. Proposed System and Architecture
6. Tools and Technologies
7. Prototype and Implementation Status
8. Testing Approach and Evidence
9. Acceptance Criteria Evaluation
10. Cross-Agent Consistency Findings
11. Limitations and Future Scope
12. Conclusion

Mandatory audits:
A. Requirements vs Architecture
- Check every FR and NFR ID.
- Identify missing or unmapped requirements.

B. Architecture vs Code
- Check whether each claimed module/component is actually supplied.
- Identify missing files, incomplete files, absent entry points, and design/code mismatches.

C. Requirements vs Tests
- Check whether each test maps to real FR/AC IDs.
- Identify requirements with no test coverage.
- Keep proposed tests separate from executed tests.

D. Code vs Documentation
- Verify file names, dependencies, setup steps, configuration, and commands.
- Report documentation claims that are not supported by the code.

E. Acceptance criteria audit — REQUIRED
For EVERY AC ID from the Requirements task, create a status row:
- Met by supplied code
- Partially met
- Not met
- Not verifiable from supplied evidence

For each row, cite the relevant FR ID and explain the evidence briefly.
Do not mark an AC as met merely because it is described in the requirements or architecture.
For example, if an AC requires admin CRUD but the supplied code has no CRUD implementation, mark it "Not met".

F. Claims and evidence
- Every implementation claim must be supported by supplied code.
- Every test execution claim must be supported by actual logs/results.
- If no execution evidence exists, state "Execution not verified; tests are proposed only."

Strict rules:
- Do not invent implementation, test results, screenshots, metrics, or successful execution.
- Do not silently resolve contradictions; list them.
- Distinguish proposed architecture, generated sample code, and verified execution.
- Do not call the whole system complete if only a prototype feature is supplied.
- The report must reflect the Testing Agent's defects and coverage findings.
- If the Testing Agent and Code Agent disagree, explain the discrepancy and use the actual supplied code as the implementation evidence.

Finish with:
1. Overall project status: Prototype / Partially implemented / Not implemented / Execution verified.
2. Three highest-priority gaps.
3. A concise release-readiness verdict.

Be precise. A truthful report is more important than a positive report.
""",
        expected_output=(
            "A 12-section academic report, a per-AC status audit, cross-agent "
            "consistency findings, evidence-based implementation status, "
            "top gaps, and a release-readiness verdict."
        ),
        agent=reporter,
        context=[task1, task2, task3, task4, task5],
    )

    return [task1, task2, task3, task4, task5, task6]
