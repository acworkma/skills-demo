# Sample No-Code Response — Medium-Risk AI Dashboard Assistant

The following example shows a realistic response from the Copilot no-code agent for a **medium-risk AI dashboard assistant** request.

---

intake_summary:  
Contoso Operations wants an internal AI dashboard assistant that helps regional managers ask natural-language questions about operational KPIs across sales, support, and fulfillment data. The solution will be used only by internal managers, will not share outputs externally, and is intended to support moderate day-to-day decision-making rather than fully automate actions.

normalized_request_type:  
ai_assistant

governance_tier:  
medium

tier_rationale:  
The request is classified as MEDIUM because it does not trigger any HIGH-tier criteria: it does not use sensitive data, does not use personal data, does not share outputs externally, and does not have high production or decision impact. It also does not qualify for LOW because the request is an internal AI assistant using multiple enterprise data sources and moderate decision support rather than a simple reporting or dashboard-only scenario.

required_reviews:
- Business Sponsor Approval
- Architecture Review
- Data Governance Review

required_controls:
- Access control policy
- Data classification
- Logging/monitoring

recommended_architecture_path:  
Azure AI Foundry project with managed endpoint, connected to governed enterprise data sources and a curated dashboard experience for internal managers.

evaluation_plan:
  metrics:
  - User satisfaction score
  - Task completion rate
  - Decision accuracy
  test_scenarios:
  - Happy-path intake submission
  - Missing-field validation
  - Edge-case classification
  responsible_ai_checks:
  - None required for this tier

approval_checklist:
- Confirm business sponsor and business owner accountability
- Confirm the normalized request type is ai_assistant
- Document all enterprise data sources used by the assistant
- Complete Architecture Review
- Complete Data Governance Review
- Define access control and data classification approach
- Confirm logging and monitoring ownership before deployment
- Review and approve the evaluation plan

open_questions:
- Which specific enterprise systems will provide the operational KPI data?
- Will the assistant expose generated summaries only, or also direct source-data drill-through?
- Are there any future plans to expand this assistant to external users or automated actions?

next_steps:
- Finalize the complete intake record with named data sources
- Schedule Architecture Review with the technical owner
- Schedule Data Governance Review for source approval and access patterns
- Draft the access control and monitoring design
- Prepare a pilot evaluation using representative manager questions

audit_metadata:
  skill_name: Project Intake & Governance Readiness
  skill_version: 1.0.0
  source: shared_skill_contract
  generated_by: Project Intake & Governance Advisor
  generated_at: 2026-06-17T16:50:21-06:00
