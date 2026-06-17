"""
Skill runtime — orchestrates evaluation of a project intake request.

This is the single entry point that both the Foundry agent and any future
Foundry Skill binding should call. All governance rules are sourced from
governance_rules.py; no logic is duplicated here.
"""

from __future__ import annotations

import logging

from .governance_rules import (
    build_approval_checklist,
    classify_tier,
    get_required_controls,
    get_required_reviews,
    recommend_architecture_path,
)
from .models import (
    AuditMetadata,
    EvaluationPlan,
    GovernanceTier,
    GovernanceReadinessResponse,
    ProjectIntakeRequest,
    RequestType,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Request-type normalization
# ---------------------------------------------------------------------------

_TYPE_ALIASES: dict[str, str] = {
    "report": RequestType.REPORTING.value,
    "reports": RequestType.REPORTING.value,
    "reporting": RequestType.REPORTING.value,
    "dashboard": RequestType.DASHBOARD.value,
    "dashboards": RequestType.DASHBOARD.value,
    "analytics": RequestType.ANALYTICS.value,
    "analytic": RequestType.ANALYTICS.value,
    "ai assistant": RequestType.AI_ASSISTANT.value,
    "ai_assistant": RequestType.AI_ASSISTANT.value,
    "assistant": RequestType.AI_ASSISTANT.value,
    "automation": RequestType.AUTOMATION.value,
    "automate": RequestType.AUTOMATION.value,
    "agentic": RequestType.AGENTIC_WORKFLOW.value,
    "agentic_workflow": RequestType.AGENTIC_WORKFLOW.value,
    "agentic workflow": RequestType.AGENTIC_WORKFLOW.value,
    "agent": RequestType.AGENTIC_WORKFLOW.value,
    "data platform": RequestType.DATA_PLATFORM.value,
    "data_platform": RequestType.DATA_PLATFORM.value,
    "copilot": RequestType.COPILOT_EXTENSION.value,
    "copilot_extension": RequestType.COPILOT_EXTENSION.value,
    "copilot extension": RequestType.COPILOT_EXTENSION.value,
}


def _normalize_request_type(raw: str) -> str:
    key = raw.lower().strip()
    return _TYPE_ALIASES.get(key, RequestType.OTHER.value)


# ---------------------------------------------------------------------------
# Evaluation plan builder
# ---------------------------------------------------------------------------

def _build_evaluation_plan(tier: GovernanceTier, normalized_type: str) -> EvaluationPlan:
    metrics = ["User satisfaction score", "Task completion rate"]
    test_scenarios = ["Happy-path intake submission", "Missing-field validation"]
    rai_checks: list[str] = []

    if tier in (GovernanceTier.MEDIUM, GovernanceTier.HIGH):
        metrics.append("Decision accuracy")
        test_scenarios.append("Edge-case classification")

    if tier == GovernanceTier.HIGH:
        metrics += ["Fairness across user groups", "Latency p95"]
        test_scenarios += [
            "Adversarial input handling",
            "PII redaction validation",
            "Human-in-the-loop escalation",
        ]
        rai_checks = [
            "Fairness evaluation",
            "Groundedness check",
            "Harmful-content filter validation",
            "Jailbreak resistance test",
        ]

    if normalized_type == RequestType.AGENTIC_WORKFLOW.value:
        test_scenarios.append("Action-rollback scenario")
        rai_checks.append("Autonomous-action boundary test")

    return EvaluationPlan(
        metrics=metrics,
        test_scenarios=test_scenarios,
        responsible_ai_checks=rai_checks,
    )


# ---------------------------------------------------------------------------
# Open questions & next steps
# ---------------------------------------------------------------------------

def _identify_open_questions(request: ProjectIntakeRequest) -> list[str]:
    questions: list[str] = []
    if request.missing_information:
        questions.append(f"Missing information noted: {request.missing_information}")
    if not request.data_sources:
        questions.append("No data sources specified — please confirm data source list.")
    if not request.preferred_platform:
        questions.append("No preferred platform specified — architecture team will recommend.")
    if request.contains_sensitive_data and not request.contains_personal_data:
        questions.append(
            "Sensitive data flagged but personal data not flagged — please confirm PII status."
        )
    return questions


def _build_next_steps(tier: GovernanceTier) -> list[str]:
    steps = [
        "Share this governance readiness package with your business sponsor.",
        "Schedule required review sessions.",
    ]
    if tier == GovernanceTier.MEDIUM:
        steps.append("Complete architecture design document before review.")
    if tier == GovernanceTier.HIGH:
        steps += [
            "Complete architecture design document before review.",
            "Submit Privacy Impact Assessment (PIA).",
            "Submit Responsible AI Impact Assessment.",
            "Prepare operational readiness checklist.",
        ]
    steps.append("Obtain all required approvals before proceeding to build.")
    return steps


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def evaluate_project_intake(request: ProjectIntakeRequest) -> GovernanceReadinessResponse:
    """Evaluate a project intake request and produce a governance readiness response.

    This function is the canonical entry point for the shared Skill. It:
      1. Normalizes the request type.
      2. Classifies the governance tier using shared rules.
      3. Determines required reviews and controls.
      4. Recommends an architecture path.
      5. Builds an evaluation plan.
      6. Generates the approval checklist, open questions, and next steps.
      7. Returns a fully-populated GovernanceReadinessResponse.
    """
    logger.info("Evaluating project intake: %s", request.request_title)

    normalized_type = _normalize_request_type(request.request_type)
    tier = classify_tier(request)

    logger.info(
        "Classification result — type: %s, tier: %s",
        normalized_type,
        tier.value,
    )

    intake_summary = (
        f"Project '{request.request_title}' submitted by {request.business_sponsor} "
        f"(business owner: {request.business_owner}, technical owner: {request.technical_owner}). "
        f"Goal: {request.business_goal}. "
        f"Type: {normalized_type}. "
        f"Target users: {request.target_users}."
    )

    tier_rationale = _build_tier_rationale(request, tier)

    return GovernanceReadinessResponse(
        intake_summary=intake_summary,
        normalized_request_type=normalized_type,
        governance_tier=tier,
        tier_rationale=tier_rationale,
        required_reviews=get_required_reviews(tier),
        required_controls=get_required_controls(tier),
        recommended_architecture_path=recommend_architecture_path(normalized_type),
        evaluation_plan=_build_evaluation_plan(tier, normalized_type),
        approval_checklist=build_approval_checklist(tier),
        open_questions=_identify_open_questions(request),
        next_steps=_build_next_steps(tier),
        audit_metadata=AuditMetadata(),
    )


def _build_tier_rationale(request: ProjectIntakeRequest, tier: GovernanceTier) -> str:
    """Explain why a particular tier was assigned."""
    reasons: list[str] = []

    if tier == GovernanceTier.HIGH:
        if request.contains_sensitive_data:
            reasons.append("contains sensitive data")
        if request.contains_personal_data:
            reasons.append("contains personal data (PII)")
        if request.external_sharing:
            reasons.append("outputs shared externally")
        if request.production_impact.lower() == "high":
            reasons.append("high production impact")
        if request.decision_impact.lower() == "high":
            reasons.append("high decision impact")
        if request.request_type.lower().strip() in ("agentic_workflow", "automation"):
            reasons.append(f"request type '{request.request_type}' requires elevated governance")
        return f"Classified as HIGH because: {'; '.join(reasons)}."

    if tier == GovernanceTier.LOW:
        return (
            "Classified as LOW because the request is an internal-only "
            "reporting/dashboard scenario with no sensitive or personal data, "
            "no external sharing, and low production and decision impact."
        )

    return (
        "Classified as MEDIUM because the request involves moderate complexity "
        "(multiple data sources, operational decision support, or internal AI assistance) "
        "but does not trigger any HIGH-tier escalation criteria."
    )
