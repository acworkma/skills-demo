# Governance Validation Checklist — Copilot No-Code Agent

Use this checklist to validate that the Copilot no-code agent stays aligned to the shared **Project Intake & Governance Readiness** Skill.

## 1. Shared Skill Contract Alignment

- [ ] The agent instructions explicitly reference the **Project Intake & Governance Readiness** Skill by name.
- [ ] The agent is described as using the shared Skill contract as the single source of truth.
- [ ] The latest shared contract version is reflected in the instructions and audit metadata.

## 2. Tiering Logic Alignment

- [ ] The instructions include: **“Do NOT invent separate governance rules.”**
- [ ] The tiering rules follow shared precedence: HIGH first, LOW second, everything else MEDIUM.
- [ ] LOW is limited to internal reporting/dashboard scenarios with no sensitive data, no personal data, no external sharing, and low production and decision impact.
- [ ] MEDIUM is used for requests that do not trigger HIGH and do not qualify for LOW, including multiple data sources or moderate decision support.
- [ ] HIGH is triggered by sensitive data, personal data, external sharing, high production impact, high decision impact, or request types `agentic_workflow` / `automation`.

## 3. Required Reviews Alignment

- [ ] LOW tier requires exactly: Business Sponsor Approval.
- [ ] MEDIUM tier requires exactly: Business Sponsor Approval, Architecture Review, Data Governance Review.
- [ ] HIGH tier requires exactly: Business Sponsor Approval, Architecture Review, Data Governance Review, Security Review, Privacy Review, Responsible AI Review, Operational Readiness Review.

## 4. Output Contract Alignment

- [ ] The agent produces all 12 output fields.
- [ ] `intake_summary` is present.
- [ ] `normalized_request_type` is present.
- [ ] `governance_tier` is present.
- [ ] `tier_rationale` is present.
- [ ] `required_reviews` is present.
- [ ] `required_controls` is present.
- [ ] `recommended_architecture_path` is present.
- [ ] `evaluation_plan` is present.
- [ ] `approval_checklist` is present.
- [ ] `open_questions` is present.
- [ ] `next_steps` is present.
- [ ] `audit_metadata` is present.

## 5. Foundry Agent Consistency

- [ ] The no-code agent does not define alternate governance tiers or extra review gates.
- [ ] The no-code agent does not conflict with the Foundry-hosted agent's governance logic.
- [ ] The no-code agent can be tested with the same sample requests used for the Foundry agent.
- [ ] The no-code agent returns the same tier outcome for equivalent inputs.

## 6. Intake Completeness Behavior

- [ ] The agent asks clarifying questions when required fields are missing.
- [ ] The agent identifies assumptions clearly when giving a preliminary assessment.
- [ ] Missing details are captured in `open_questions`.

## 7. Audit Metadata

- [ ] `audit_metadata.skill_name` is `Project Intake & Governance Readiness`.
- [ ] `audit_metadata.skill_version` is `1.0.0`.
- [ ] `audit_metadata.source` references the shared Skill contract.
- [ ] `audit_metadata.generated_by` identifies the Copilot no-code agent.
- [ ] `audit_metadata.generated_at` is included as an ISO 8601 timestamp.

## 8. Demo Readiness

- [ ] The README documents both Copilot Studio and Agent Builder deployment paths.
- [ ] Conversation starters are configured in the no-code agent experience.
- [ ] A sample response is available for demo rehearsal.
- [ ] The team can explain this as **the same Skill, two agent experiences**.
