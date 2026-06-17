import re
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
PACKAGE_DIR = SRC_DIR / "governance_foundry_agent"

for import_path in (SRC_DIR, PACKAGE_DIR):
    import_path_str = str(import_path)
    if import_path_str not in sys.path:
        sys.path.insert(0, import_path_str)


MAIN_SOURCE = (PROJECT_ROOT / "src" / "governance_foundry_agent" / "main.py").read_text(
    encoding="utf-8"
)
RULES_SOURCE = (
    PROJECT_ROOT / "src" / "governance_foundry_agent" / "shared_skill" / "governance_rules.py"
).read_text(encoding="utf-8")
INSTRUCTIONS_SOURCE = (
    PROJECT_ROOT / "copilot_no_code" / "declarative_agent_instructions.md"
).read_text(encoding="utf-8")


def test_foundry_agent_main_imports_the_shared_skill_contract() -> None:
    assert "from shared_skill.models import ProjectIntakeRequest" in MAIN_SOURCE
    assert "from shared_skill.report_renderer import render_markdown_summary" in MAIN_SOURCE
    assert "from shared_skill.skill_runtime import evaluate_project_intake" in MAIN_SOURCE


def test_foundry_agent_main_does_not_duplicate_tiering_logic() -> None:
    assert "def classify_tier" not in MAIN_SOURCE
    assert "_AGENTIC_TYPES" not in MAIN_SOURCE
    assert '_LOW_RISK_TYPES = {"reporting", "dashboard"}' not in MAIN_SOURCE
    assert 'production_impact == "high"' not in MAIN_SOURCE
    assert 'decision_impact == "high"' not in MAIN_SOURCE
    assert "Do NOT invent or override governance logic." in MAIN_SOURCE


def test_copilot_instructions_reference_the_shared_skill_name() -> None:
    assert "Project Intake & Governance Readiness" in INSTRUCTIONS_SOURCE


def test_copilot_instructions_reference_same_tier_criteria_as_shared_rules() -> None:
    expected_rule_phrases = [
        "Contains sensitive data (`contains_sensitive_data == true`)",
        "Contains personal data / PII (`contains_personal_data == true`)",
        "Outputs are shared externally (`external_sharing == true`)",
        'Production impact is high (`production_impact == "high"`)',
        'Decision impact is high (`decision_impact == "high"`)',
        "Request type is `agentic_workflow` or `automation`",
        "Request type is `reporting` or `dashboard`",
        "No sensitive data (`contains_sensitive_data == false`)",
        "No personal data (`contains_personal_data == false`)",
        "No external sharing (`external_sharing == false`)",
        'Production impact is low (`production_impact == "low"`)',
        'Decision impact is low (`decision_impact == "low"`)',
    ]

    assert "Rules are evaluated top-down. The first matching tier wins." in INSTRUCTIONS_SOURCE
    for phrase in expected_rule_phrases:
        assert phrase in INSTRUCTIONS_SOURCE

    assert re.search(r"def classify_tier", RULES_SOURCE) is not None
    assert "Do NOT invent separate governance rules." in INSTRUCTIONS_SOURCE
    assert "critical tier" not in INSTRUCTIONS_SOURCE.lower()


def test_copilot_instructions_mention_all_output_contract_fields() -> None:
    expected_output_fields = [
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
    ]

    for field_name in expected_output_fields:
        assert f"`{field_name}`" in INSTRUCTIONS_SOURCE
