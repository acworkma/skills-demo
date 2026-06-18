# Governance Rules — Project Intake & Governance Readiness Skill

## Governance Tier Definitions

The Skill assigns every project request to exactly one of three governance tiers. Rules are evaluated **top-down** — the first matching tier wins.

### 🔴 HIGH Tier

A request is classified as **HIGH** if **any** of the following are true:

- Contains sensitive data (`contains_sensitive_data == true`)
- Contains personal data / PII (`contains_personal_data == true`)
- Outputs are shared externally (`external_sharing == true`)
- Production impact is high (`production_impact == "high"`)
- Decision impact is high (`decision_impact == "high"`)
- Request type is `agentic_workflow` or `automation`

**Required reviews:** Business Sponsor Approval, Architecture Review, Data Governance Review, Security Review, Privacy Review, Responsible AI Review, Operational Readiness Review

**Required controls:** Access control policy defined, Data classification documented, Logging and monitoring enabled, Encryption at rest and in transit, PII handling procedures documented, Responsible AI impact assessment completed, Incident response plan documented, Audit trail enabled, Human-in-the-loop safeguards for agentic actions

### 🟡 MEDIUM Tier

A request is classified as **MEDIUM** if it does **not** trigger any HIGH criteria, and does **not** qualify for LOW.

Typical characteristics:
- Multiple enterprise data sources
- Moderate operational decision support
- Automation or internal AI assistance
- Does not trigger HIGH-tier escalation

**Required reviews:** Business Sponsor Approval, Architecture Review, Data Governance Review

**Required controls:** Access control policy defined, Data classification documented, Logging and monitoring enabled

### 🟢 LOW Tier

A request is classified as **LOW** only if **all** of the following are true:

- Request type is `reporting` or `dashboard`
- No sensitive data (`contains_sensitive_data == false`)
- No personal data (`contains_personal_data == false`)
- No external sharing (`external_sharing == false`)
- Production impact is low (`production_impact == "low"`)
- Decision impact is low (`decision_impact == "low"`)

**Required reviews:** Business Sponsor Approval

**Required controls:** None

## Rule Precedence

```
HIGH triggers are checked first → if any match → HIGH
LOW criteria checked second    → if all match  → LOW
Everything else                                → MEDIUM
```

## Architecture Recommendations by Type

| Request Type | Recommended Path |
|---|---|
| `reporting` | Power BI / Fabric workspace with governed dataset |
| `dashboard` | Power BI / Fabric workspace with governed dataset |
| `analytics` | Azure Synapse / Fabric lakehouse with governed access |
| `ai_assistant` | Azure AI Foundry project with managed endpoint |
| `automation` | Azure Logic Apps / Power Automate with approval gates |
| `agentic_workflow` | Azure AI Foundry hosted agent with human-in-the-loop controls |
| `data_platform` | Microsoft Fabric / Azure Data Factory with lineage tracking |
| `copilot_extension` | Microsoft 365 Copilot declarative agent with Foundry Skill |
| `other` | Consult Enterprise Architecture team for custom path |

## Single Source of Truth

These rules are implemented in `src/governance_foundry_agent/shared_skill/governance_rules.py` and referenced (not duplicated) by:

1. **Foundry hosted agent** — calls `classify_tier()`, `get_required_reviews()`, `get_required_controls()` from the shared module
2. **Copilot no-code agent** — instructions reference these same rules via the Skill contract; the agent does **not** define its own conflicting governance logic
