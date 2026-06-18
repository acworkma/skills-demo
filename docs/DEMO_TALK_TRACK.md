# 🗣️ Demo Talk Track

> **Audience**: Enterprise customers, architects, and IT leaders evaluating Azure AI Foundry.
>
> **Duration**: 10–15 minutes (adjust by skipping optional sections).
>
> **Key message**: Define governance rules once as a Foundry Skill, publish them to a Toolbox, and every agent — pro-code or no-code — discovers and follows the same rules automatically.

---

## Act 1 — The Problem (2 min)

> **What to say**:
>
> "Every enterprise has governance rules — who approves a project, what reviews are required, what controls must be in place. Today, those rules get copy-pasted into every bot, every copilot, every custom agent. When a policy changes, you're updating five different codebases. Worse, they drift. Your Copilot agent says a project needs two reviews while your pro-code agent says three."

**Show**: Open `copilot_no_code/declarative_agent_instructions.md` and scroll through the governance rules. Point out how long and detailed they are.

> "Now imagine maintaining this across dozens of agents. That's the problem Foundry Skills solve."

---

## Act 2 — The Skill: Define Once (2 min)

> **What to say**:
>
> "A Foundry Skill is a versioned, centrally-managed piece of behavioral guidance. Think of it as a policy document that agents can discover and consume at runtime — not embedded in code, not copy-pasted."

**Show in the Foundry portal**:
1. Navigate to **Build → Tools → Skills**.
2. Click on `project-intake-governance` and show the Skill content — the input contract (18 fields), the tiering rules (low/medium/high), the required reviews, and the output contract.

> "This Skill defines everything: what information to collect from a project submitter, how to classify risk, what reviews and controls are required, and what the output package looks like. It's authored once and versioned."

---

## Act 3 — The Toolbox: Publish as MCP (2 min)

> **What to say**:
>
> "A Skill sitting in a registry is useful, but how do agents find it? That's what a Toolbox does. A Toolbox is an MCP endpoint — Model Context Protocol — that any client can connect to and discover available skills and tools."

**Show in the Foundry portal**:
1. Navigate to **Build → Tools → Toolboxes**.
2. Click on `governance-toolbox` and show the Skill attached to it.
3. Copy the MCP endpoint URL and display it.

> "Any MCP-compatible client — a hosted Foundry agent, Copilot Studio, Claude Code, GitHub Copilot, LangGraph — can connect to this single endpoint and discover every skill and tool we've published. No SDK required, no special integration. It's an open protocol."

**Show the MCP endpoint URL format**:
```
https://<account>.services.ai.azure.com/api/projects/<project>/toolboxes/governance-toolbox/mcp?api-version=v1
```

---

## Act 4 — Pro-Code Agent: Consume via MCP (3 min)

> **What to say**:
>
> "Let's see this in action. Here's a hosted Foundry agent — a Python container running in Azure. At startup, it connects to the Toolbox MCP endpoint and loads the governance Skill."

**Show in code** (`src/governance_foundry_agent/main.py`):
1. Show the `_load_skill_from_toolbox()` function — it connects to the Toolbox via MCP, calls `resources/list` to discover skills, then `read_resource` to download the Skill content.
2. Show `_build_instructions()` — the downloaded Skill content gets injected into the agent's system prompt.
3. Show the `evaluate_governance` tool — a local Python function that executes the governance rules deterministically (not LLM-dependent).

> "The agent's behavior comes from the Skill. The execution comes from the Python module. If the governance rules change, we update the Skill in Foundry — not the agent code."

**Live demo**: Invoke the agent with a sample project idea.

```
I want to build an AI-powered customer support chatbot that accesses our
CRM database with customer PII and will be available on our public website.
```

The agent asks clarifying questions to fill in the required fields. Provide the follow-up answers:

```
Here are the details:

- Project name: Customer Support AI Chatbot
- Description: An AI chatbot integrated with our Salesforce CRM that answers
  customer questions about their orders, accounts, and billing. It accesses
  customer PII including names, emails, and order history.
- Business sponsor: Sarah Chen, VP of Customer Experience
- Business owner: Marcus Johnson, Director of Support Operations
- Technical owner: Priya Patel, Lead Platform Engineer
- Target users: External customers visiting our public support portal
- Business goal: Reduce support ticket volume by 40% and improve first-response
  time from 4 hours to under 2 minutes
- Request type: ai_assistant
- Data sources: Salesforce CRM, Zendesk ticket history
- Contains sensitive data: yes
- Contains personal data: yes
- External sharing: yes
- Production impact: high
- Decision impact: medium
```

Show the response — it should classify as **HIGH** tier with security, privacy, and responsible AI reviews required.

---

## Act 5 — No-Code Agent: Same Rules, Different UX (2 min)

> **What to say**:
>
> "Not every team writes Python. A business analyst might build a Copilot agent in the Microsoft 365 Copilot Studio GUI. Can they use the same governance rules? Yes."

**Show**: Open `copilot_no_code/README_DEPLOY_COPILOT_GUI.md` and walk through the setup.

> "Today, Copilot agents consume the governance rules by pasting the Skill instructions into the agent's system prompt. But because the Toolbox is a standard MCP endpoint, Copilot Studio can connect to it directly — discovering the same governance Skill without any copy-paste."

**(Optional)** If Copilot Studio is available, show the MCP connector configuration pointing to the Toolbox endpoint.

---

## Act 6 — The Payoff: Define Once, Reuse Everywhere (2 min)

> **What to say**:
>
> "Let's step back and look at what we've built."

**Show the architecture diagram** from the README:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Azure AI Foundry Project                     │
│                                                                 │
│   ┌─────────────────────┐    ┌──────────────────────────────┐  │
│   │ Registered Skill    │───▶│ Toolbox (MCP endpoint)       │  │
│   │ (governance rules)  │    │ governance-toolbox            │  │
│   └─────────────────────┘    └──────┬───────────┬───────────┘  │
│                                     │           │               │
│                          ┌──────────▼──┐  ┌─────▼──────────┐   │
│                          │ Hosted Agent │  │ Copilot Studio │   │
│                          │ (Python)     │  │ (MCP client)   │   │
│                          └─────────────┘  └────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                                │
                     ┌──────────▼──────────┐
                     │ No-Code Copilot     │
                     │ (manual rules)      │
                     └─────────────────────┘
```

> "One Skill definition. One Toolbox endpoint. Three different agent experiences — all following the same governance rules. When the rules change, you update the Skill, create a new Toolbox version, and every agent picks up the change automatically. No redeployment needed."

---

## Closing (1 min)

> "This is the pattern we recommend for any enterprise policy that crosses agent boundaries: compliance checks, approval workflows, data classification, security posture, operational readiness. Define the logic once as a Skill, publish it through a Toolbox, and let every agent — regardless of how it's built — discover and follow the same rules."

---

## 📄 Sample Output

After invoking the agent, you can compare the output against these references:

- [`samples/expected_markdown_summary.md`](../samples/expected_markdown_summary.md) — Expected markdown summary
- [`samples/expected_skill_response.json`](../samples/expected_skill_response.json) — Expected structured JSON response
- [`samples/high_risk_agentic_workflow_request.json`](../samples/high_risk_agentic_workflow_request.json) — High-risk sample input
- [`samples/low_risk_reporting_request.json`](../samples/low_risk_reporting_request.json) — Low-risk sample input
