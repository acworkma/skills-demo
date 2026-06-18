"""Hosted Foundry agent for project intake governance evaluation.

Connects to a Foundry Toolbox via MCP to discover and load the governance
Skill at runtime, then uses the local shared_skill module to execute
governance evaluations.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os

import httpx
from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
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

# Fallback instructions used when the Toolbox MCP Skill is unreachable.
FALLBACK_INSTRUCTIONS = f"""
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


def _load_skill_from_toolbox() -> str | None:
    """Load governance Skill instructions from the Foundry Toolbox via MCP.

    Returns the Skill content as a string, or None if the toolbox is
    unavailable (in which case the agent falls back to bundled instructions).
    """
    toolbox_name = os.environ.get("TOOLBOX_NAME", "governance-toolbox")
    project_endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT", "")
    if not project_endpoint:
        logger.warning("FOUNDRY_PROJECT_ENDPOINT not set — skipping Toolbox Skill load")
        return None

    toolbox_url = (
        f"{project_endpoint.rstrip('/')}/toolboxes/{toolbox_name}"
        f"/mcp?api-version=v1"
    )
    logger.info("Connecting to Toolbox MCP: %s", toolbox_url)

    try:
        from mcp import ClientSession
        from mcp.client.streamable_http import streamablehttp_client
    except ImportError:
        logger.warning("mcp package not installed — skipping Toolbox Skill load")
        return None

    async def _fetch() -> str | None:
        credential = DefaultAzureCredential()
        token = credential.get_token("https://ai.azure.com/.default").token
        headers = {
            "Authorization": f"Bearer {token}",
            "Foundry-Features": "Toolboxes=V1Preview",
        }
        async with streamablehttp_client(toolbox_url, headers=headers) as (
            read,
            write,
            _,
        ):
            async with ClientSession(read, write) as session:
                await session.initialize()
                resources = await session.list_resources()
                for resource in resources.resources:
                    if "project-intake-governance" in str(resource.uri):
                        content = await session.read_resource(resource.uri)
                        if content.contents:
                            text = content.contents[0].text
                            logger.info(
                                "Loaded Skill from Toolbox (%d chars)",
                                len(text),
                            )
                            return text
        return None

    try:
        return asyncio.run(_fetch())
    except Exception:
        logger.warning("Failed to load Skill from Toolbox", exc_info=True)
        return None


def _build_instructions(skill_content: str | None) -> str:
    """Build agent instructions from Toolbox Skill or fallback."""
    preamble = (
        "You are the Governance Intake Agent for project readiness assessments.\n\n"
        "Accept natural-language project intake requests and gather the information "
        "needed to build a complete ProjectIntakeRequest package. Ask clarifying "
        "questions when required fields are missing or ambiguous. The required "
        f"fields are: {', '.join(REQUIRED_FIELDS)}.\n\n"
        "When you have enough information, call the evaluate_governance tool with a "
        "JSON string that matches the ProjectIntakeRequest schema. Use the tool "
        "output to produce the final answer.\n\n"
        "Always return:\n"
        "1. A concise conversational summary of the governance outcome.\n"
        "2. The structured package from the tool.\n"
        "3. The markdown summary from the tool.\n\n"
    )
    if skill_content:
        return (
            preamble
            + "## Governance Skill (loaded from Foundry Toolbox)\n\n"
            + skill_content
            + "\n\nDo NOT invent or override governance logic. "
            "The Skill above is the single source of truth."
        )
    return FALLBACK_INSTRUCTIONS


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
    # Load governance Skill from Foundry Toolbox (falls back to bundled instructions)
    skill_content = _load_skill_from_toolbox()
    if skill_content:
        logger.info("Using governance Skill loaded from Foundry Toolbox.")
    else:
        logger.info("Using bundled fallback instructions (Toolbox unavailable).")

    instructions = _build_instructions(skill_content)

    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        credential=DefaultAzureCredential(),
    )

    agent = Agent(
        client=client,
        name="governance-intake-agent",
        instructions=instructions,
        tools=[evaluate_governance],
        default_options={"store": False},
    )

    server = ResponsesHostServer(agent)
    server.run()


if __name__ == "__main__":
    main()
