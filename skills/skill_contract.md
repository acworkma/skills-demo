# Skill Contract — Project Intake & Governance Readiness

This document describes the input and output contracts for the **Project Intake & Governance Readiness** Skill. Both the Foundry hosted agent and the Copilot no-code agent use these contracts.

## Input Contract (18 Fields)

| # | Field | Type | Required | Description |
|---|-------|------|----------|-------------|
| 1 | `request_title` | string | ✅ | Short title for the project request |
| 2 | `request_description` | string | ✅ | Detailed description of the request |
| 3 | `business_sponsor` | string | ✅ | Executive sponsor name |
| 4 | `business_owner` | string | ✅ | Day-to-day business owner |
| 5 | `technical_owner` | string | ✅ | Technical lead or architect |
| 6 | `target_users` | string | ✅ | Who will use the solution |
| 7 | `business_goal` | string | ✅ | Business outcome or KPI this supports |
| 8 | `request_type` | string | ✅ | Category (see values below) |
| 9 | `data_sources` | array[string] | ❌ | Data sources involved |
| 10 | `contains_sensitive_data` | boolean | ✅ | Does the solution use sensitive data? |
| 11 | `contains_personal_data` | boolean | ✅ | Does the solution use personal data (PII)? |
| 12 | `external_sharing` | boolean | ✅ | Will outputs be shared externally? |
| 13 | `production_impact` | string | ✅ | Production impact: `low` \| `medium` \| `high` |
| 14 | `decision_impact` | string | ✅ | Decision impact: `low` \| `medium` \| `high` |
| 15 | `urgency` | string | ❌ | Urgency: `low` \| `medium` \| `high` \| `critical` (default: `medium`) |
| 16 | `preferred_platform` | string | ❌ | Preferred platform (e.g., Azure AI Foundry, Databricks) |
| — | `known_constraints` | string | ❌ | Known constraints or blockers |
| — | `missing_information` | string | ❌ | Information still needed |

### Valid `request_type` Values

`reporting` · `dashboard` · `analytics` · `ai_assistant` · `automation` · `agentic_workflow` · `data_platform` · `copilot_extension` · `other`

## Output Contract (12 Fields)

| # | Field | Type | Description |
|---|-------|------|-------------|
| 1 | `intake_summary` | string | Plain-language summary of the request |
| 2 | `normalized_request_type` | string | Normalized request category |
| 3 | `governance_tier` | string | Risk tier: `low` \| `medium` \| `high` |
| 4 | `tier_rationale` | string | Why this tier was assigned |
| 5 | `required_reviews` | array[string] | Required review gates |
| 6 | `required_controls` | array[string] | Required controls and safeguards |
| 7 | `recommended_architecture_path` | string | Suggested architecture approach |
| 8 | `evaluation_plan` | object | Metrics, test scenarios, responsible AI checks |
| 9 | `approval_checklist` | array[string] | Items to complete before approval |
| 10 | `open_questions` | array[string] | Unresolved questions |
| 11 | `next_steps` | array[string] | Recommended next actions |
| 12 | `audit_metadata` | object | Skill name, version, timestamp, source |

## Contract Versioning

The contracts are versioned in `project_intake_governance_skill.yaml`. The current version is **1.0.0**. Changes to input or output fields require a version bump and updates to both the Foundry agent and Copilot agent instructions.
