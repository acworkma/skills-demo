# 🗣️ Demo Talk Track

Use this narrative for a 3–5 minute customer demo:

1. Start with the business problem: governance logic often gets duplicated across bots, copilots, and custom apps.
2. Open the Foundry portal and show the registered **Skill** under Build → Tools → Skills.
3. Show the Foundry hosted agent and how it calls the shared runtime through `evaluate_governance`.
4. Show the no-code Copilot agent instructions and highlight that they reference the same contract and rules.
5. Close with the key value proposition: **define once, reuse everywhere**.

---

## ▶️ Suggested Live Demo Flow

1. Open the Foundry portal and show the registered Skill under **Build → Tools → Skills**.
2. Open `skills/project_intake_governance_skill.yaml` and point out the shared input/output contract.
3. Open `src/governance_foundry_agent/main.py` and show the tool registration.
4. Invoke the Foundry hosted agent with a sample project idea.
5. Show the generated readiness package and markdown summary.
6. Open the Copilot no-code deployment guide and explain the alternate user experience.
7. If available, show the Copilot agent producing the same governance outcome for the same request.
8. End by comparing both channels and reinforcing that the business rules were not duplicated.

---

## 📄 Sample Output

See the expected markdown summary here:

- [`samples/expected_markdown_summary.md`](../samples/expected_markdown_summary.md)

You can also compare the structured output in:

- [`samples/expected_skill_response.json`](../samples/expected_skill_response.json)
