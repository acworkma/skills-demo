"""
Register the Project Intake & Governance Readiness Skill in Azure AI Foundry
and publish it to a Toolbox for MCP-based discovery.

Usage:
    python scripts/register_skill.py

Requires:
    - FOUNDRY_PROJECT_ENDPOINT environment variable (or passed via azd env)
    - Azure CLI authentication (DefaultAzureCredential)
    - pip install azure-ai-projects azure-identity
"""

import os
import sys

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import SkillInlineContent, ToolboxSkillReference
from azure.identity import DefaultAzureCredential

SKILL_NAME = "project-intake-governance"
TOOLBOX_NAME = "governance-toolbox"

DESCRIPTION = (
    "Standardize project intake, classification, governance tiering, "
    "required review identification, evaluation planning, and approval "
    "readiness for analytics and AI project proposals. Define governance "
    "rules once and reuse across pro-code Foundry agents and no-code "
    "Copilot agents."
)

INSTRUCTIONS = """\
You are the Project Intake & Governance Readiness Skill.

Your purpose: Standardize project intake, classification, governance tiering, \
required review identification, evaluation planning, and approval readiness \
for analytics and AI project proposals.

## Input Contract (18 Fields)
Accept these fields from the user (ask clarifying questions for any missing required fields):
- request_title (required), request_description (required), business_sponsor (required), \
business_owner (required), technical_owner (required), target_users (required), \
business_goal (required), request_type (required: reporting|dashboard|analytics|\
ai_assistant|automation|agentic_workflow|data_platform|copilot_extension|other), \
data_sources (list), contains_sensitive_data (boolean, required), \
contains_personal_data (boolean, required), external_sharing (boolean, required), \
production_impact (required: low|medium|high), decision_impact (required: low|medium|high), \
urgency (low|medium|high|critical), preferred_platform, known_constraints, missing_information

## Governance Tier Classification Rules (evaluate top-down, first match wins)

### HIGH — any of:
- contains_sensitive_data is true
- contains_personal_data is true
- external_sharing is true
- production_impact == "high"
- decision_impact == "high"
- request_type is agentic_workflow or automation

### LOW — all of:
- request_type is reporting or dashboard
- No sensitive or personal data
- No external sharing
- production_impact == "low"
- decision_impact == "low"

### MEDIUM — everything else

## Required Reviews by Tier
- LOW: Business Sponsor Approval
- MEDIUM: Business Sponsor Approval, Architecture Review, Data Governance Review
- HIGH: Business Sponsor Approval, Architecture Review, Data Governance Review, \
Security Review, Privacy Review, Responsible AI Review, Operational Readiness Review

## Required Controls by Tier
- LOW: None
- MEDIUM: Access control policy defined, Data classification documented, \
Logging and monitoring enabled
- HIGH: Access control policy defined, Data classification documented, \
Logging and monitoring enabled, Encryption at rest and in transit, \
PII handling procedures documented, Responsible AI impact assessment completed, \
Incident response plan documented, Audit trail enabled, \
Human-in-the-loop safeguards for agentic actions

## Output Contract (12 Fields)
Always produce ALL of these fields in your response:
1. intake_summary - Plain-language summary
2. normalized_request_type - Normalized category
3. governance_tier - low|medium|high
4. tier_rationale - Why this tier was assigned
5. required_reviews - List of required review gates
6. required_controls - List of required controls
7. recommended_architecture_path - Suggested architecture approach
8. evaluation_plan - Metrics, test scenarios, responsible AI checks
9. approval_checklist - Items to complete before approval
10. open_questions - Unresolved questions
11. next_steps - Recommended next actions
12. audit_metadata - Skill name, version (1.0.0), timestamp, source (shared_skill)

## Architecture Recommendations by Type
- reporting/dashboard: Power BI / Fabric workspace with governed dataset
- analytics: Azure Synapse / Fabric lakehouse with governed access
- ai_assistant: Azure AI Foundry project with managed endpoint
- automation: Azure Logic Apps / Power Automate with approval gates
- agentic_workflow: Azure AI Foundry hosted agent with human-in-the-loop controls
- data_platform: Microsoft Fabric / Azure Data Factory with lineage tracking
- copilot_extension: Microsoft 365 Copilot declarative agent with Foundry Skill

Do NOT invent separate governance rules. These rules are the single source of truth.
"""


def main():
    endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
    if not endpoint:
        print("ERROR: FOUNDRY_PROJECT_ENDPOINT environment variable is not set.")
        print("Set it to your Foundry project endpoint, e.g.:")
        print("  export FOUNDRY_PROJECT_ENDPOINT=https://<account>.services.ai.azure.com/api/projects/<project>")
        sys.exit(1)

    client = AIProjectClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential(),
    )

    # Step 1: Register the Skill
    print(f"Registering Skill '{SKILL_NAME}'...")
    skill = client.beta.skills.create(
        name=SKILL_NAME,
        inline_content=SkillInlineContent(
            description=DESCRIPTION,
            instructions=INSTRUCTIONS,
        ),
        default=True,
    )
    print(f"  Skill registered: {skill.name} (version {skill.version})")

    # Step 2: Publish the Skill to a Toolbox
    print(f"\nPublishing Skill to Toolbox '{TOOLBOX_NAME}'...")
    toolbox_version = client.beta.toolboxes.create_version(
        name=TOOLBOX_NAME,
        description=(
            "Governance toolbox providing the Project Intake & Governance "
            "Readiness Skill via MCP. Connect any agent — hosted, Copilot "
            "Studio, or external MCP client — to this endpoint to discover "
            "and consume governance skills."
        ),
        tools=[],
        skills=[ToolboxSkillReference(name=SKILL_NAME)],
    )
    print(f"  Toolbox version created: {toolbox_version.version}")

    # Build the MCP endpoint URL
    mcp_endpoint = f"{endpoint.rstrip('/')}/toolboxes/{TOOLBOX_NAME}/mcp?api-version=v1"
    print(f"\nToolbox MCP endpoint (for agents and Copilot Studio):")
    print(f"  {mcp_endpoint}")
    print()
    print("The Skill is visible in the Foundry portal under Build > Tools > Skills.")
    print("The Toolbox is visible under Build > Tools > Toolboxes.")
    print()
    print("To connect a hosted agent or Copilot Studio, use the MCP endpoint above.")
    print("Required header: Foundry-Features: Toolboxes=V1Preview")


if __name__ == "__main__":
    main()
