"""Pydantic models for the Project Intake & Governance Readiness Skill contracts."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class GovernanceTier(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RequestType(str, Enum):
    REPORTING = "reporting"
    DASHBOARD = "dashboard"
    ANALYTICS = "analytics"
    AI_ASSISTANT = "ai_assistant"
    AUTOMATION = "automation"
    AGENTIC_WORKFLOW = "agentic_workflow"
    DATA_PLATFORM = "data_platform"
    COPILOT_EXTENSION = "copilot_extension"
    OTHER = "other"


class Urgency(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ---------------------------------------------------------------------------
# Input contract — 16 fields
# ---------------------------------------------------------------------------

class ProjectIntakeRequest(BaseModel):
    """Input contract for the Project Intake & Governance Readiness Skill."""

    request_title: str = Field(..., description="Short title for the project request")
    request_description: str = Field(..., description="Detailed description of the request")
    business_sponsor: str = Field(..., description="Executive sponsor name")
    business_owner: str = Field(..., description="Day-to-day business owner")
    technical_owner: str = Field(..., description="Technical lead or architect")
    target_users: str = Field(..., description="Who will use the solution")
    business_goal: str = Field(..., description="Business outcome or KPI this supports")
    request_type: str = Field(
        ...,
        description="Category: reporting, dashboard, analytics, ai_assistant, "
        "automation, agentic_workflow, data_platform, copilot_extension, other",
    )
    data_sources: list[str] = Field(default_factory=list, description="Data sources involved")
    contains_sensitive_data: bool = Field(False, description="Does the solution use sensitive data?")
    contains_personal_data: bool = Field(False, description="Does the solution use personal data (PII)?")
    external_sharing: bool = Field(False, description="Will outputs be shared externally?")
    production_impact: str = Field("low", description="Production impact: low, medium, high")
    decision_impact: str = Field("low", description="Decision impact: low, medium, high")
    urgency: str = Field("medium", description="Urgency: low, medium, high, critical")
    preferred_platform: str = Field("", description="Preferred platform (e.g., Azure AI Foundry, Databricks)")
    known_constraints: Optional[str] = Field(None, description="Known constraints or blockers")
    missing_information: Optional[str] = Field(None, description="Information still needed")


# ---------------------------------------------------------------------------
# Output contract — 12 fields
# ---------------------------------------------------------------------------

class EvaluationPlan(BaseModel):
    """Evaluation expectations for the governance readiness package."""

    metrics: list[str] = Field(default_factory=list)
    test_scenarios: list[str] = Field(default_factory=list)
    responsible_ai_checks: list[str] = Field(default_factory=list)


class AuditMetadata(BaseModel):
    """Audit trail metadata attached to every governance assessment."""

    skill_name: str = "Project Intake & Governance Readiness"
    skill_version: str = "1.0.0"
    assessed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source: str = "shared_skill"


class GovernanceReadinessResponse(BaseModel):
    """Output contract for the Project Intake & Governance Readiness Skill."""

    intake_summary: str = Field(..., description="Plain-language summary of the request")
    normalized_request_type: str = Field(..., description="Normalized request category")
    governance_tier: GovernanceTier = Field(..., description="Risk tier: low, medium, high")
    tier_rationale: str = Field(..., description="Why this tier was assigned")
    required_reviews: list[str] = Field(default_factory=list, description="Required review gates")
    required_controls: list[str] = Field(default_factory=list, description="Required controls")
    recommended_architecture_path: str = Field("", description="Suggested architecture approach")
    evaluation_plan: EvaluationPlan = Field(default_factory=EvaluationPlan)
    approval_checklist: list[str] = Field(default_factory=list, description="Checklist items for approval")
    open_questions: list[str] = Field(default_factory=list, description="Unresolved questions")
    next_steps: list[str] = Field(default_factory=list, description="Recommended next actions")
    audit_metadata: AuditMetadata = Field(default_factory=AuditMetadata)
