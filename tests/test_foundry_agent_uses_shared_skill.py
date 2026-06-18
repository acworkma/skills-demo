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
SKILL_REGISTRATION_SOURCE = (
    PROJECT_ROOT / "scripts" / "register_skill.py"
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
    """Copilot Studio instructions delegate to the Toolbox Skill for governance
    rules. Verify the instructions reference the Skill and do NOT duplicate
    tier criteria inline. The actual tier criteria live in the registered Skill
    (scripts/register_skill.py INSTRUCTIONS constant)."""

    # Instructions should reference the Toolbox as the source of truth
    assert "Toolbox" in INSTRUCTIONS_SOURCE
    assert "Do NOT invent separate governance rules." in INSTRUCTIONS_SOURCE
    assert "single source of truth" in INSTRUCTIONS_SOURCE

    # Instructions should NOT contain the full tiering rules (they come from the Skill)
    assert "Rules are evaluated top-down" not in INSTRUCTIONS_SOURCE
    assert "contains_sensitive_data == true" not in INSTRUCTIONS_SOURCE

    # The registered Skill SHOULD contain the full tiering rules
    assert "contains_sensitive_data is true" in SKILL_REGISTRATION_SOURCE
    assert "contains_personal_data is true" in SKILL_REGISTRATION_SOURCE
    assert "external_sharing is true" in SKILL_REGISTRATION_SOURCE
    assert "agentic_workflow" in SKILL_REGISTRATION_SOURCE

    # The Python governance_rules module should have the classify_tier function
    assert re.search(r"def classify_tier", RULES_SOURCE) is not None


def test_copilot_instructions_mention_all_output_contract_fields() -> None:
    """The registered Skill (not the Copilot instructions) should list all 12
    output contract fields. The Copilot instructions just say 'return the full
    12-field readiness package' and let the Skill define the fields."""

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

    # The registered Skill should list all 12 fields
    for field_name in expected_output_fields:
        assert field_name in SKILL_REGISTRATION_SOURCE, (
            f"Registered Skill missing output field: {field_name}"
        )

    # Copilot instructions should reference the 12-field package concept
    assert "12" in INSTRUCTIONS_SOURCE
    assert "output" in INSTRUCTIONS_SOURCE.lower() or "readiness package" in INSTRUCTIONS_SOURCE
