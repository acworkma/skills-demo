# Shared Governance Skill for Foundry and Copilot Agents

[![Azure Developer CLI](https://img.shields.io/badge/azd-%3E%3D1.25.2-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/developer/azure-developer-cli/)
[![Azure AI Foundry](https://img.shields.io/badge/Azure%20AI-Foundry-5C2D91?logo=microsoft&logoColor=white)](https://learn.microsoft.com/azure/ai-foundry/)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)

## 🎯 Demo Purpose

This demo shows how **one shared governance Skill** can define intake rules, risk tiering, required reviews, controls, and output contracts **once**—then be reused by:

- a **pro-code Azure AI Foundry hosted agent**, and
- a **no-code Copilot agent**.

The result is consistent governance behavior across both experiences, without duplicating business rules.

## ✨ Why Azure AI Foundry Skills Matter

Azure AI Foundry Skills enable teams to **define a business capability once and reuse it across multiple agents**. In this demo, the shared Skill is the governance source of truth for:

- project intake requirements,
- governance tier classification,
- review and control requirements,
- evaluation expectations, and
- standardized readiness outputs.

That means less drift, less duplicated logic, and a cleaner path to scaling agent experiences across channels.

## 🏗️ Architecture

```mermaid
flowchart LR
    U1[Business User / Requestor]
    U2[Copilot User]

    S[(Shared Governance Skill<br/>project_intake_governance_skill.yaml<br/>+ Python runtime contract)]

    subgraph F[Azure AI Foundry Project]
        M[Model Deployment<br/>gpt-4.1-mini]
        A[Foundry Hosted Agent<br/>governance-intake-agent]
    end

    C[Copilot No-Code Agent<br/>Project Intake & Governance Advisor]

    U1 --> A
    U2 --> C
    A --> S
    C --> S
    A --> M
    A --> U1
    C --> U2
```

## 📁 Project Structure

```text
.
├── azure.yaml                                 # azd project definition for the hosted Foundry agent
├── infra/
│   └── main.bicep                            # Minimal azd-compatible infrastructure entry point
├── skills/
│   ├── project_intake_governance_skill.yaml  # Shared Skill contract and governance tier definitions
│   ├── skill_contract.md                     # Human-readable Skill contract
│   ├── governance_rules.md                   # Governance logic and policy guidance
│   └── evaluation_expectations.md            # Evaluation and review expectations
├── src/
│   └── governance_foundry_agent/
│       ├── main.py                           # Hosted Foundry agent entry point
│       ├── agent.yaml                        # Hosted agent template
│       ├── agent.manifest.yaml               # Foundry agent manifest
│       ├── requirements.txt                  # Python dependencies
│       ├── Dockerfile                        # Container image definition
│       ├── .env.example                      # Local environment variable template
│       └── shared_skill/
│           ├── skill_runtime.py              # Canonical evaluation entry point
│           ├── governance_rules.py           # Tiering, controls, and review logic
│           ├── models.py                     # Pydantic request/response models
│           └── report_renderer.py            # Markdown summary renderer
├── copilot_no_code/
│   ├── README_DEPLOY_COPILOT_GUI.md          # GUI deployment walkthrough for the no-code agent
│   ├── declarative_agent_instructions.md     # Shared governance-aligned instructions
│   ├── conversation_starters.md              # Suggested demo prompts
│   └── governance_checklist.md               # Validation guidance for no-code outputs
├── samples/
│   ├── expected_markdown_summary.md          # Expected demo-ready markdown output
│   ├── expected_skill_response.json          # Expected structured response
│   └── *_request.json                        # Sample intake requests
└── tests/                                    # Test folder referenced by the demo command
```

## 🤖 How the Foundry Agent Works

The Foundry agent in `src/governance_foundry_agent/main.py` is a pro-code hosted agent built with **agent-framework**:

1. It imports the shared models and runtime from `shared_skill`.
2. It registers `evaluate_governance` as a tool.
3. The tool validates input against `ProjectIntakeRequest`.
4. The shared runtime evaluates the request using centralized governance rules.
5. The agent returns both a structured package and a markdown summary.

This keeps the governance logic in one place while allowing the hosted agent to provide conversational intake and tool-based execution.

## 🧩 How the Copilot Agent Works

The no-code Copilot experience uses declarative instructions that point back to the **same Skill contract and governance rules**. Its instructions explicitly tell the agent to:

- align to the shared request schema,
- apply the same low / medium / high tiering rules,
- return the same 12-field readiness package, and
- avoid inventing alternate governance policies.

This gives you two different user experiences with one governance definition.

## 🚀 Quick Start — Deploy the Foundry Agent

### 1) Prerequisites

- Python 3.13
- `azd` version `>= 1.25.2`
- Azure subscription access
- An Azure AI Foundry project (or permission to create one)

### 2) Install the Foundry extension

```bash
azd ext install microsoft.foundry
```

### 3) Initialize the agent definition

Run this from `src/governance_foundry_agent`:

```bash
azd ai agent init -m agent.manifest.yaml --deploy-mode code
```

### 4) Configure environment variables

Copy `.env.example` to `.env` in `src/governance_foundry_agent` and set:

- `FOUNDRY_PROJECT_ENDPOINT`
- `AZURE_AI_MODEL_DEPLOYMENT_NAME`

### 5) Provision infrastructure if needed

If you are creating a new Foundry-backed environment:

```bash
azd provision
```

If you already have the required Foundry project and supporting Azure resources, you can skip this step.

### 6) Deploy the hosted agent

```bash
azd deploy
```

### 7) Invoke the demo

```bash
azd ai agent invoke "I want to submit a new AI project for governance review"
```

## 🪄 Quick Start — Configure the Copilot Agent

For the no-code Copilot experience, follow the guided walkthrough in:

`copilot_no_code/README_DEPLOY_COPILOT_GUI.md`

That guide covers both:

- **Copilot Studio** for richer runtime integration, and
- **Agent Builder** for a lighter instructions-first experience.

## 🗣️ Demo Talk Track

Use this narrative for a 3–5 minute customer demo:

1. Start with the business problem: governance logic often gets duplicated across bots, copilots, and custom apps.
2. Show the shared Skill YAML and explain that it is the single governance contract.
3. Show the Foundry hosted agent and how it calls the shared runtime through `evaluate_governance`.
4. Show the no-code Copilot agent instructions and highlight that they reference the same contract and rules.
5. Close with the key value proposition: **define once, reuse everywhere**.

## ▶️ Suggested Live Demo Flow

1. Open `skills/project_intake_governance_skill.yaml` and point out the shared input/output contract.
2. Open `src/governance_foundry_agent/main.py` and show the tool registration.
3. Invoke the Foundry hosted agent with a sample project idea.
4. Show the generated readiness package and markdown summary.
5. Open the Copilot no-code deployment guide and explain the alternate user experience.
6. If available, show the Copilot agent producing the same governance outcome for the same request.
7. End by comparing both channels and reinforcing that the business rules were not duplicated.

## 📄 Sample Output

See the expected markdown summary here:

- `samples/expected_markdown_summary.md`

You can also compare the structured output in:

- `samples/expected_skill_response.json`

## ✅ Running Tests

```bash
pip install pydantic pytest && pytest tests/ -v
```

## 🧹 Cleanup

To tear down provisioned resources:

```bash
azd down
```

## 📌 Important Notes

- All data in this demo is **synthetic**—no real customers, projects, or companies are represented.
- This demo targets **modern Azure AI Foundry projects (Microsoft Foundry)**, not legacy hub-based patterns.
- **Foundry Skills are currently in preview**; until the GA SDK surface is available, the Python shared module serves as the runtime implementation.

## 🤝 Summary

This repository demonstrates a practical pattern for enterprise agent governance: **one shared Skill, multiple agent experiences, consistent outcomes**.
