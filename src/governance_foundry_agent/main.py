"""Hosted Foundry agent for project intake governance evaluation."""

from __future__ import annotations

import json
import logging
import os

from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

from shared_skill.models import ProjectIntakeRequest
from shared_skill.report_renderer import render_markdown_summary
from shared_skill.skill_runtime import evaluate_project_intake

load_dotenv(override=False)

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper())
logger = logging.getLogger(__name__)

REQUIRED_FIELDS = [
    "request_title",
    "request_description",
    "business_sponsor",
    "business_owner",
    "technical_owner",
    "target_users",
    "business_goal",
    "request_type",
]

AGENT_INSTRUCTIONS = f"""
You are the Governance Intake Agent for project readiness assessments.

Accept natural-language project intake requests and gather the information needed
to build a complete ProjectIntakeRequest package. Ask clarifying questions when
required fields are missing or ambiguous. The required fields are:
{", ".join(REQUIRED_FIELDS)}.

When you have enough information, call the evaluate_governance tool with a JSON
string that matches the ProjectIntakeRequest schema. Use the tool output to
produce the final answer.

Always return:
1. A concise conversational summary of the governance outcome.
2. The structured package from the tool.
3. The markdown summary from the tool.

Governance rules are loaded from the shared Project Intake & Governance Readiness Skill. Do NOT invent or override governance logic.
""".strip()


@tool(
    name="evaluate_governance",
    description=(
        "Evaluate a project intake request from a JSON string and return both "
        "the structured governance readiness package and a markdown summary."
    ),
)
async def evaluate_governance(request_json: str) -> str:
    """Run the shared governance evaluator on a ProjectIntakeRequest payload."""
    request = ProjectIntakeRequest.model_validate_json(request_json)
    response = evaluate_project_intake(request)
    return json.dumps(
        {
            "structured_package": response.model_dump(mode="json"),
            "markdown_summary": render_markdown_summary(response),
        },
        indent=2,
    )


def main() -> None:
    """Start the hosted agent server."""
    logger.info("Governance rules loaded from the shared skill module.")

    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        credential=DefaultAzureCredential(),
    )

    agent = Agent(
        client=client,
        name="governance-intake-agent",
        instructions=AGENT_INSTRUCTIONS,
        tools=[evaluate_governance],
        default_options={"store": False},
    )

    server = ResponsesHostServer(agent)
    server.run()


if __name__ == "__main__":
    main()
