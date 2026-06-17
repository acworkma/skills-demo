"""Render a GovernanceReadinessResponse as a Markdown summary."""

from __future__ import annotations

from .models import GovernanceReadinessResponse


def render_markdown_summary(response: GovernanceReadinessResponse) -> str:
    """Convert a governance readiness response into a human-readable Markdown report."""
    lines: list[str] = []

    lines.append(f"# Governance Readiness Report")
    lines.append("")
    lines.append(f"## Intake Summary")
    lines.append("")
    lines.append(response.intake_summary)
    lines.append("")

    lines.append(f"## Classification")
    lines.append("")
    lines.append(f"| Field | Value |")
    lines.append(f"|---|---|")
    lines.append(f"| **Request Type** | {response.normalized_request_type} |")
    lines.append(f"| **Governance Tier** | {response.governance_tier.value.upper()} |")
    lines.append("")
    lines.append(f"**Tier Rationale:** {response.tier_rationale}")
    lines.append("")

    if response.recommended_architecture_path:
        lines.append(f"## Recommended Architecture Path")
        lines.append("")
        lines.append(response.recommended_architecture_path)
        lines.append("")

    if response.required_reviews:
        lines.append(f"## Required Reviews")
        lines.append("")
        for review in response.required_reviews:
            lines.append(f"- [ ] {review}")
        lines.append("")

    if response.required_controls:
        lines.append(f"## Required Controls")
        lines.append("")
        for control in response.required_controls:
            lines.append(f"- [ ] {control}")
        lines.append("")

    if response.evaluation_plan.metrics or response.evaluation_plan.test_scenarios:
        lines.append(f"## Evaluation Plan")
        lines.append("")
        if response.evaluation_plan.metrics:
            lines.append("### Metrics")
            lines.append("")
            for m in response.evaluation_plan.metrics:
                lines.append(f"- {m}")
            lines.append("")
        if response.evaluation_plan.test_scenarios:
            lines.append("### Test Scenarios")
            lines.append("")
            for t in response.evaluation_plan.test_scenarios:
                lines.append(f"- {t}")
            lines.append("")
        if response.evaluation_plan.responsible_ai_checks:
            lines.append("### Responsible AI Checks")
            lines.append("")
            for r in response.evaluation_plan.responsible_ai_checks:
                lines.append(f"- {r}")
            lines.append("")

    if response.approval_checklist:
        lines.append(f"## Approval Checklist")
        lines.append("")
        for item in response.approval_checklist:
            lines.append(f"- [ ] {item}")
        lines.append("")

    if response.open_questions:
        lines.append(f"## Open Questions")
        lines.append("")
        for q in response.open_questions:
            lines.append(f"- ⚠️ {q}")
        lines.append("")

    if response.next_steps:
        lines.append(f"## Next Steps")
        lines.append("")
        for i, step in enumerate(response.next_steps, 1):
            lines.append(f"{i}. {step}")
        lines.append("")

    lines.append(f"---")
    lines.append(f"*Assessed by: {response.audit_metadata.skill_name} "
                 f"v{response.audit_metadata.skill_version} | "
                 f"Source: {response.audit_metadata.source} | "
                 f"Timestamp: {response.audit_metadata.assessed_at}*")
    lines.append("")

    return "\n".join(lines)
