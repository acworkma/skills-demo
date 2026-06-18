# Deploy the Copilot Studio Agent — GUI Walkthrough

This guide shows how to create a Copilot Studio agent that connects to the **Foundry Toolbox MCP endpoint** to consume the shared **Project Intake & Governance Readiness** Skill at runtime. The agent discovers and loads the governance rules automatically — no copy-pasting of rules required.

---

## Prerequisites

- An active **Microsoft 365 Copilot** license.
- Access to **Copilot Studio** (https://copilotstudio.microsoft.com).
- Permission to create or publish Copilot agents in your tenant.
- The **Foundry Toolbox MCP endpoint** URL (printed by `scripts/register_skill.py` during deployment).
- The conversation starters from `copilot_no_code/conversation_starters.md`.

---

## Step 1 — Open Copilot Studio

1. Go to **https://copilotstudio.microsoft.com**.
2. Sign in with your Microsoft 365 account.

## Step 2 — Create a new agent

1. In the left navigation, select **Agents**.
2. Choose **Microsoft 365 Copilot**.
3. Select **Add agent**.

## Step 3 — Enter the core agent details

- **Name**: `Project Intake & Governance Advisor`
- **Description**:
  `Helps teams submit project ideas, classify governance risk, identify required reviews and controls, and generate a standardized readiness package using the shared governance Skill from the Foundry Toolbox.`

## Step 4 — Paste the instructions

1. Open `copilot_no_code/declarative_agent_instructions.md`.
2. Copy the text under **Instructions (paste into Copilot Studio → Instructions field)**.
3. Paste it into the agent **Instructions** field.

These instructions are intentionally short — they tell the agent its role and to follow the Skill from the Toolbox. The governance rules themselves are loaded at runtime via MCP.

## Step 5 — Connect the Foundry Toolbox (MCP)

This is the key step that connects the Copilot Studio agent to the same governance Skill used by the hosted Foundry agent.

1. In the agent configuration, select **Add Tool**.
2. Choose **Model Context Protocol**.
3. Fill in the fields on the **Add a Model Context Protocol server** screen:

| Field | Value |
|-------|-------|
| **Server name** | `Governance Toolbox` |
| **Server description** | `Foundry Toolbox providing the Project Intake & Governance Readiness Skill for governance tiering, required reviews, controls, and readiness output.` |
| **Server URL** | `https://<account>.services.ai.azure.com/api/projects/<project>/toolboxes/governance-toolbox/mcp?api-version=v1` |
| **Authentication** | Select **OAuth 2.0** and configure with your Entra ID app registration (scope: `https://ai.azure.com/.default`). If testing locally, **None** may work with a browser-authenticated session. |

4. Click **Create**.

The agent now discovers the `project-intake-governance` Skill from the Toolbox at runtime — the same Skill the hosted Foundry agent uses.

## Step 6 — Add conversation starters

1. Open `copilot_no_code/conversation_starters.md`.
2. Add the starter titles and prompt text as the agent's suggested prompts.
3. Include at least 6 starters so demo users can quickly test multiple scenarios.

## Step 7 — Test the agent

1. Open the built-in **test chat**.
2. Try a reporting scenario, an AI assistant scenario, and an agentic workflow scenario.
3. Verify the agent:
   - asks for missing required fields,
   - classifies governance tier correctly (LOW / MEDIUM / HIGH),
   - returns the full 12-field readiness package,
   - includes audit metadata referencing the Skill.

## Step 8 — Publish

1. Review the agent configuration.
2. Select **Publish**.
3. Confirm the publish target and availability settings for your tenant.

---

## Validation — Same Skill, Two Agent Experiences

Use the same scenario in both the hosted Foundry agent and the Copilot Studio agent, then compare outputs:

1. Pick a sample request (e.g., a high-risk agentic workflow from `samples/`).
2. Submit the same project details to both agents.
3. Confirm both produce:
   - the same governance tier,
   - the same required reviews and controls,
   - all 12 output fields, and
   - audit metadata referencing the shared Skill.

If the outputs differ, the Copilot Studio agent may not have the MCP connection configured correctly — check Step 5.

---

## Troubleshooting

### The agent invents governance rules not in the Skill

- Verify the MCP tool connection points to the correct Toolbox endpoint.
- Confirm the instructions include: **"Do NOT invent separate governance rules."**

### The agent does not ask for missing information

- Confirm the instructions tell the agent to ask clarifying questions for missing required fields.
- Test with an intentionally incomplete request.

### The agent does not return all 12 output fields

- Verify the Skill content is loading from the Toolbox (check MCP connection status).
- Re-paste the instructions from `declarative_agent_instructions.md`.

### The Copilot Studio agent behaves differently from the Foundry agent

- Verify the MCP endpoint URL matches the one printed by `scripts/register_skill.py`.
- Confirm the Toolbox version is current (the Skill may have been updated).
- Retest with a known sample prompt from `conversation_starters.md`.
