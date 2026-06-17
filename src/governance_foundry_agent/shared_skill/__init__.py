"""
Shared Skill: Project Intake & Governance Readiness

This module is the single source of truth for governance classification,
risk tiering, required reviews, and output contracts. Both the pro-code
Foundry agent and the no-code Copilot agent consume these rules.

Do NOT duplicate governance logic outside this module.
"""

from .models import ProjectIntakeRequest, GovernanceReadinessResponse
from .governance_rules import classify_tier, get_required_reviews, get_required_controls
from .skill_runtime import evaluate_project_intake
from .report_renderer import render_markdown_summary

__all__ = [
    "ProjectIntakeRequest",
    "GovernanceReadinessResponse",
    "classify_tier",
    "get_required_reviews",
    "get_required_controls",
    "evaluate_project_intake",
    "render_markdown_summary",
]
