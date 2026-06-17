# Deploy the Copilot No-Code Agent — GUI Walkthrough

This guide shows how to create a customer-ready no-code Copilot experience for the shared **Project Intake & Governance Readiness** Skill. The goal is to preserve the same governance logic, same tiering outcomes, and same 12-field readiness package used by the Foundry-hosted agent.

## Positioning

Position this solution as **the same Skill, delivered through two agent experiences**:

- **Path A — Copilot Studio**: best when you want richer configuration and runtime tool integration to the shared Foundry Skill.
- **Path B — Agent Builder**: best when you want a fast instructions-only experience inside Microsoft 365 Copilot.

In both cases, the governance source of truth remains the shared Skill contract in `skills\project_intake_governance_skill.yaml`, `skills\skill_contract.md`, and `skills\governance_rules.md`.

---

## Prerequisites

Before creating the agent, confirm:

- You have an active **Microsoft 365 Copilot** license.
- You have access to **Copilot Studio** for the recommended integration path.
- You have permission to create or publish Copilot agents in your tenant.
- You have the finalized instructions from `copilot_no_code\declarative_agent_instructions.md`.
- You have the conversation starters from `copilot_no_code\conversation_starters.md`.
- If using runtime Skill integration, you have the **Foundry Toolbox MCP endpoint** details available.
- You know who will validate the agent output against the Foundry-hosted agent.

---

## Path A — Copilot Studio (Recommended for Full Skill Integration)

Use this path when you want the no-code agent to connect to the shared Foundry Skill at runtime through MCP.

### 1) Open Copilot Studio

1. Go to **https://copilotstudio.microsoft.com**
2. Sign in with your Microsoft 365 account.

### 2) Create a new agent

1. In the left navigation, select **Agents**.
2. Choose **Microsoft 365 Copilot**.
3. Select **Add agent**.

### 3) Enter the core agent details

Use the following values:

- **Name**: `Project Intake & Governance Advisor`
- **Description**:  
  `Helps teams submit project ideas, classify governance risk, identify required reviews and controls, and generate a standardized readiness package using the shared Project Intake & Governance Readiness Skill.`

### 4) Paste the declarative instructions

1. Open `copilot_no_code\declarative_agent_instructions.md`.
2. Copy the full contents.
3. Paste the text into the agent **Instructions** field.

### 5) Add suggested prompts / conversation starters

1. Open `copilot_no_code\conversation_starters.md`.
2. Add the starter titles and prompt text as the agent's suggested prompts.
3. Include at least 6 starters so demo users can quickly test multiple scenarios.

### 6) Add the runtime Skill integration

This is the recommended pattern for sharing the same runtime governance behavior as the Foundry-hosted agent.

1. In the agent configuration, select **Add Tool**.
2. Choose **Model Context Protocol**.
3. Enter the **Foundry Toolbox MCP endpoint** for the shared Skill runtime.
4. Save the tool connection.

**Important:** This MCP connection is the integration path that lets the Copilot Studio agent connect to the shared Foundry Skill at runtime instead of inventing separate governance behavior.

### 7) Test the agent

1. Open the built-in **test chat**.
2. Try a reporting scenario, an AI assistant scenario, and an agentic workflow scenario.
3. Verify the agent:
   - asks for missing required fields,
   - uses LOW / MEDIUM / HIGH correctly,
   - returns the full 12-field readiness package,
   - includes audit metadata.

### 8) Publish

1. Review the agent configuration one final time.
2. Select **Publish**.
3. Confirm the publish target and availability settings for your tenant.

---

## Path B — Agent Builder (Simpler, Instructions-Only)

Use this path when you want a lightweight Microsoft 365 Copilot experience without MCP tool wiring.

### 1) Open Agent Builder

1. Go to **https://microsoft365.com/chat**
2. Sign in with your Microsoft 365 account.
3. Select **Create agent**.

### 2) Configure the agent

Use the same core values:

- **Name**: `Project Intake & Governance Advisor`
- **Description**:  
  `Helps teams submit project ideas, classify governance risk, identify required reviews and controls, and generate a standardized readiness package using the shared Project Intake & Governance Readiness Skill.`

### 3) Paste the instructions

1. Open `copilot_no_code\declarative_agent_instructions.md`.
2. Copy the full text.
3. Paste it into the **Instructions** field.

### 4) Add knowledge sources if needed

If your tenant experience supports knowledge sources, add the supporting governance references so the agent can stay aligned:

- `skills\skill_contract.md`
- `skills\governance_rules.md`
- `copilot_no_code\governance_checklist.md`

### 5) Test the experience

1. Run a few example prompts from `copilot_no_code\conversation_starters.md`.
2. Confirm the agent asks clarifying questions before final classification when required fields are missing.
3. Confirm the response follows the standardized 12-field format.

### 6) Create

1. When testing looks good, select **Create**.
2. Share the new agent with your intended demo audience.

---

## How to Validate the Copilot Agent Produces the Same Output Contract as the Foundry Agent

Use the same scenario in both experiences and compare outputs side by side.

### Recommended validation process

1. Pick a sample request, such as a medium-risk AI dashboard assistant.
2. Submit the exact same project details to:
   - the **Foundry-hosted agent**, and
   - the **Copilot no-code agent**.
3. Confirm both produce the same 12 output fields:
   1. `intake_summary`
   2. `normalized_request_type`
   3. `governance_tier`
   4. `tier_rationale`
   5. `required_reviews`
   6. `required_controls`
   7. `recommended_architecture_path`
   8. `evaluation_plan`
   9. `approval_checklist`
   10. `open_questions`
   11. `next_steps`
   12. `audit_metadata`
4. Confirm the governance tier is identical.
5. Confirm the required reviews match the shared rules exactly.
6. Confirm the audit metadata references the shared Skill and version.

### Acceptance criteria

The Copilot no-code agent is aligned if it:

- uses the same governance tier as the Foundry agent,
- applies the same required reviews and controls,
- does not invent alternate governance policies,
- returns all 12 output fields consistently.

---

## How to Position This as “Same Skill, Two Agent Experiences”

Use this message in demos and customer conversations:

> We defined the governance logic once in the Project Intake & Governance Readiness Skill. From there, we expose it through two user experiences: a Foundry-hosted pro-code agent and a Microsoft 365 Copilot no-code agent. The experience differs, but the contract, tiering rules, review requirements, and readiness package stay the same.

Key talking points:

- **One governance policy** shared across channels
- **Different surfaces** for different user needs
- **Consistent classification and approvals**
- **Lower drift risk** because the no-code experience references the same Skill contract

---

## Troubleshooting Tips

### The agent gives a tier but skips required reviews

- Recheck that the full instructions from `declarative_agent_instructions.md` were pasted.
- Confirm the response template still includes all 12 fields.

### The agent invents new governance policies

- Confirm the instructions still include: **“Do NOT invent separate governance rules.”**
- If using knowledge sources, ensure only the shared governance documents are attached.

### The Copilot Studio agent does not behave like the Foundry agent

- Verify the **Model Context Protocol** tool points to the correct **Foundry Toolbox MCP endpoint**.
- Confirm the shared Skill version matches the documentation.
- Retest with a known sample prompt from `conversation_starters.md`.

### The agent does not ask for missing information

- Confirm the instructions explicitly tell the agent to ask clarifying questions for missing required fields.
- Test with an intentionally incomplete request.

### The output format is inconsistent

- Re-paste the output template from `declarative_agent_instructions.md`.
- Validate against `governance_checklist.md`.

### The no-code experience is too limited for advanced integration

- Use **Path A — Copilot Studio** and wire the agent to the MCP endpoint.
- Position **Path B — Agent Builder** as a lighter-weight instructions-first experience.
