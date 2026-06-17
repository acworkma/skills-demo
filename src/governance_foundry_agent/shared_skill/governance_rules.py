"""
Governance classification rules — single source of truth.

These rules are consumed by both the Foundry hosted agent and the Copilot
no-code agent (via the shared Skill contract). Do NOT duplicate this logic.
"""

from __future__ import annotations

from .models import GovernanceTier, ProjectIntakeRequest


# ---------------------------------------------------------------------------
# Tier classification
# ---------------------------------------------------------------------------

# Request types that always escalate to HIGH
_AGENTIC_TYPES = {"agentic_workflow", "automation"}

# Request types typically LOW risk when data flags are clean
_LOW_RISK_TYPES = {"reporting", "dashboard"}


def classify_tier(request: ProjectIntakeRequest) -> GovernanceTier:
    """Determine the governance tier for a project intake request.

    Rules (evaluated top-down — first match wins):
      HIGH — any of:
        • contains_sensitive_data is True
        • contains_personal_data is True
        • external_sharing is True
        • production_impact == "high"
        • decision_impact == "high"
        • request_type is agentic_workflow or automation
      LOW — all of:
        • request_type is reporting or dashboard
        • no sensitive/personal data
        • no external sharing
        • production_impact == "low"
        • decision_impact == "low"
      MEDIUM — everything else
    """
    rt = request.request_type.lower().strip()

    # --- HIGH triggers ---
    if request.contains_sensitive_data:
        return GovernanceTier.HIGH
    if request.contains_personal_data:
        return GovernanceTier.HIGH
    if request.external_sharing:
        return GovernanceTier.HIGH
    if request.production_impact.lower() == "high":
        return GovernanceTier.HIGH
    if request.decision_impact.lower() == "high":
        return GovernanceTier.HIGH
    if rt in _AGENTIC_TYPES:
        return GovernanceTier.HIGH

    # --- LOW triggers ---
    if (
        rt in _LOW_RISK_TYPES
        and not request.contains_sensitive_data
        and not request.contains_personal_data
        and not request.external_sharing
        and request.production_impact.lower() == "low"
        and request.decision_impact.lower() == "low"
    ):
        return GovernanceTier.LOW

    # --- Everything else ---
    return GovernanceTier.MEDIUM


# ---------------------------------------------------------------------------
# Required reviews
# ---------------------------------------------------------------------------

_BASE_REVIEWS = ["Business Sponsor Approval"]

_MEDIUM_REVIEWS = [
    "Architecture Review",
    "Data Governance Review",
]

_HIGH_REVIEWS = [
    "Architecture Review",
    "Data Governance Review",
    "Security Review",
    "Privacy Review",
    "Responsible AI Review",
    "Operational Readiness Review",
]


def get_required_reviews(tier: GovernanceTier) -> list[str]:
    """Return the list of required review gates for the given tier."""
    if tier == GovernanceTier.LOW:
        return list(_BASE_REVIEWS)
    if tier == GovernanceTier.MEDIUM:
        return _BASE_REVIEWS + _MEDIUM_REVIEWS
    return _BASE_REVIEWS + _HIGH_REVIEWS


# ---------------------------------------------------------------------------
# Required controls
# ---------------------------------------------------------------------------

_MEDIUM_CONTROLS = [
    "Access control policy defined",
    "Data classification documented",
    "Logging and monitoring enabled",
]

_HIGH_CONTROLS = [
    "Access control policy defined",
    "Data classification documented",
    "Logging and monitoring enabled",
    "Encryption at rest and in transit",
    "PII handling procedures documented",
    "Responsible AI impact assessment completed",
    "Incident response plan documented",
    "Audit trail enabled",
    "Human-in-the-loop safeguards for agentic actions",
]


def get_required_controls(tier: GovernanceTier) -> list[str]:
    """Return the list of required controls for the given tier."""
    if tier == GovernanceTier.LOW:
        return []
    if tier == GovernanceTier.MEDIUM:
        return list(_MEDIUM_CONTROLS)
    return list(_HIGH_CONTROLS)


# ---------------------------------------------------------------------------
# Architecture path recommendation
# ---------------------------------------------------------------------------

_ARCHITECTURE_PATHS: dict[str, str] = {
    "reporting": "Power BI / Fabric workspace with governed dataset",
    "dashboard": "Power BI / Fabric workspace with governed dataset",
    "analytics": "Azure Synapse / Fabric lakehouse with governed access",
    "ai_assistant": "Azure AI Foundry project with managed endpoint",
    "automation": "Azure Logic Apps / Power Automate with approval gates",
    "agentic_workflow": "Azure AI Foundry hosted agent with human-in-the-loop controls",
    "data_platform": "Microsoft Fabric / Azure Data Factory with lineage tracking",
    "copilot_extension": "Microsoft 365 Copilot declarative agent with Foundry Skill",
}


def recommend_architecture_path(request_type: str) -> str:
    """Suggest an architecture approach based on normalized request type."""
    return _ARCHITECTURE_PATHS.get(
        request_type.lower().strip(),
        "Consult Enterprise Architecture team for custom path",
    )


# ---------------------------------------------------------------------------
# Approval checklist
# ---------------------------------------------------------------------------

def build_approval_checklist(tier: GovernanceTier) -> list[str]:
    """Generate the approval checklist based on tier."""
    checklist = [
        "Business case documented",
        "Data sources identified",
        "Target users confirmed",
    ]
    if tier in (GovernanceTier.MEDIUM, GovernanceTier.HIGH):
        checklist += [
            "Architecture design reviewed",
            "Data governance sign-off obtained",
        ]
    if tier == GovernanceTier.HIGH:
        checklist += [
            "Security review completed",
            "Privacy impact assessment completed",
            "Responsible AI review completed",
            "Operational readiness confirmed",
            "Monitoring and alerting configured",
            "Incident response plan approved",
        ]
    return checklist
