import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
PACKAGE_DIR = SRC_DIR / "governance_foundry_agent"

for import_path in (SRC_DIR, PACKAGE_DIR):
    import_path_str = str(import_path)
    if import_path_str not in sys.path:
        sys.path.insert(0, import_path_str)

from governance_foundry_agent.shared_skill.models import (  # noqa: E402
    GovernanceReadinessResponse,
    ProjectIntakeRequest,
)
from governance_foundry_agent.shared_skill.skill_runtime import evaluate_project_intake  # noqa: E402


def load_sample(name: str) -> dict:
    return json.loads((PROJECT_ROOT / "samples" / name).read_text(encoding="utf-8"))


def test_project_intake_request_contract_has_all_expected_fields() -> None:
    expected_fields = {
        "request_title",
        "request_description",
        "business_sponsor",
        "business_owner",
        "technical_owner",
        "target_users",
        "business_goal",
        "request_type",
        "data_sources",
        "contains_sensitive_data",
        "contains_personal_data",
        "external_sharing",
        "production_impact",
        "decision_impact",
        "urgency",
        "preferred_platform",
        "known_constraints",
        "missing_information",
    }
    required_fields = {
        "request_title",
        "request_description",
        "business_sponsor",
        "business_owner",
        "technical_owner",
        "target_users",
        "business_goal",
        "request_type",
    }

    actual_fields = set(ProjectIntakeRequest.model_fields)

    assert len(actual_fields) >= 16
    assert actual_fields == expected_fields
    assert {
        name for name, field in ProjectIntakeRequest.model_fields.items() if field.is_required()
    } == required_fields


def test_governance_readiness_response_contract_has_all_expected_fields() -> None:
    expected_fields = {
        "intake_summary",
        "normalized_request_type",
        "governance_tier",
        "tier_rationale",
        "required_reviews",
        "required_controls",
        "recommended_architecture_path",
        "evaluation_plan",
        "approval_checklist",
        "open_questions",
        "next_steps",
        "audit_metadata",
    }

    assert set(GovernanceReadinessResponse.model_fields) == expected_fields


def test_valid_request_can_be_serialized_and_deserialized() -> None:
    request = ProjectIntakeRequest.model_validate(load_sample("low_risk_reporting_request.json"))

    serialized = request.model_dump_json()
    round_tripped = ProjectIntakeRequest.model_validate_json(serialized)

    assert round_tripped == request


def test_output_contract_includes_audit_metadata_fields() -> None:
    request = ProjectIntakeRequest.model_validate(load_sample("medium_risk_ai_dashboard_assistant_request.json"))

    response = evaluate_project_intake(request).model_dump(mode="json")
    audit_metadata = response["audit_metadata"]

    assert audit_metadata["skill_name"] == "Project Intake & Governance Readiness"
    assert audit_metadata["skill_version"] == "1.0.0"
    assert audit_metadata["source"] == "shared_skill"


def test_evaluate_project_intake_returns_populated_response() -> None:
    request = ProjectIntakeRequest.model_validate(load_sample("high_risk_agentic_workflow_request.json"))

    response = evaluate_project_intake(request)

    assert isinstance(response, GovernanceReadinessResponse)
    assert response.intake_summary
    assert response.normalized_request_type == "agentic_workflow"
    assert response.governance_tier.value == "high"
    assert response.tier_rationale
    assert response.required_reviews
    assert response.recommended_architecture_path
    assert response.evaluation_plan.metrics
    assert response.approval_checklist
    assert response.next_steps
    assert response.audit_metadata.skill_name == "Project Intake & Governance Readiness"

