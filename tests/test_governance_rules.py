import json
import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
PACKAGE_DIR = SRC_DIR / "governance_foundry_agent"

for import_path in (SRC_DIR, PACKAGE_DIR):
    import_path_str = str(import_path)
    if import_path_str not in sys.path:
        sys.path.insert(0, import_path_str)

from governance_foundry_agent.shared_skill.models import ProjectIntakeRequest  # noqa: E402
from governance_foundry_agent.shared_skill.skill_runtime import evaluate_project_intake  # noqa: E402


def load_sample(name: str) -> dict:
    return json.loads((PROJECT_ROOT / "samples" / name).read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    ("sample_name", "expected_tier"),
    [
        ("low_risk_reporting_request.json", "low"),
        ("medium_risk_ai_dashboard_assistant_request.json", "medium"),
        ("high_risk_agentic_workflow_request.json", "high"),
    ],
)
def test_sample_requests_classify_into_expected_tiers(sample_name: str, expected_tier: str) -> None:
    request = ProjectIntakeRequest.model_validate(load_sample(sample_name))

    response = evaluate_project_intake(request)

    assert response.governance_tier.value == expected_tier


def test_low_tier_has_only_business_sponsor_approval_review() -> None:
    request = ProjectIntakeRequest.model_validate(load_sample("low_risk_reporting_request.json"))

    response = evaluate_project_intake(request)

    assert response.governance_tier.value == "low"
    assert response.required_reviews == ["Business Sponsor Approval"]


def test_medium_tier_includes_architecture_and_data_governance_reviews() -> None:
    request = ProjectIntakeRequest.model_validate(
        load_sample("medium_risk_ai_dashboard_assistant_request.json")
    )

    response = evaluate_project_intake(request)

    assert response.governance_tier.value == "medium"
    assert "Architecture Review" in response.required_reviews
    assert "Data Governance Review" in response.required_reviews


def test_high_tier_includes_required_governance_reviews() -> None:
    request = ProjectIntakeRequest.model_validate(load_sample("high_risk_agentic_workflow_request.json"))

    response = evaluate_project_intake(request)

    assert response.governance_tier.value == "high"
    for review in (
        "Security Review",
        "Privacy Review",
        "Responsible AI Review",
        "Operational Readiness Review",
    ):
        assert review in response.required_reviews


def test_high_tier_includes_agentic_human_in_the_loop_control() -> None:
    request = ProjectIntakeRequest.model_validate(load_sample("high_risk_agentic_workflow_request.json"))

    response = evaluate_project_intake(request)

    assert "Human-in-the-loop safeguards for agentic actions" in response.required_controls


def test_low_tier_required_controls_are_empty() -> None:
    request = ProjectIntakeRequest.model_validate(load_sample("low_risk_reporting_request.json"))

    response = evaluate_project_intake(request)

    assert response.required_controls == []


def test_agentic_workflow_type_always_triggers_high_even_without_sensitive_flags() -> None:
    sample = load_sample("high_risk_agentic_workflow_request.json")
    sample.update(
        {
            "contains_sensitive_data": False,
            "contains_personal_data": False,
            "external_sharing": False,
            "production_impact": "low",
            "decision_impact": "low",
        }
    )
    request = ProjectIntakeRequest.model_validate(sample)

    response = evaluate_project_intake(request)

    assert request.request_type == "agentic_workflow"
    assert response.governance_tier.value == "high"

