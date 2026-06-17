# Evaluation Expectations — Project Intake & Governance Readiness Skill

## Overview

Every governance readiness assessment includes an evaluation plan. The depth of evaluation scales with the governance tier.

## Evaluation Metrics

| Tier | Metrics |
|------|---------|
| LOW | User satisfaction score, Task completion rate |
| MEDIUM | User satisfaction score, Task completion rate, Decision accuracy |
| HIGH | User satisfaction score, Task completion rate, Decision accuracy, Fairness across user groups, Latency p95 |

## Test Scenarios

| Tier | Scenarios |
|------|-----------|
| LOW | Happy-path intake submission, Missing-field validation |
| MEDIUM | Happy-path intake submission, Missing-field validation, Edge-case classification |
| HIGH | Happy-path intake submission, Missing-field validation, Edge-case classification, Adversarial input handling, PII redaction validation, Human-in-the-loop escalation |

### Additional Scenarios by Request Type

| Request Type | Additional Scenario |
|---|---|
| `agentic_workflow` | Action-rollback scenario |

## Responsible AI Checks (HIGH Tier Only)

- Fairness evaluation
- Groundedness check
- Harmful-content filter validation
- Jailbreak resistance test

### Additional RAI Checks by Request Type

| Request Type | Additional Check |
|---|---|
| `agentic_workflow` | Autonomous-action boundary test |

## Evaluation Workflow

1. **Pre-deployment**: Run all test scenarios against the Skill locally using sample requests in `samples/`.
2. **Post-deployment**: Monitor metrics in production using Azure AI Foundry evaluation tools.
3. **Periodic review**: Re-run responsible AI checks quarterly or after significant model/rule changes.

## Connecting to Azure AI Foundry Evaluations

When deployed to Azure AI Foundry, connect evaluation expectations to the built-in evaluation framework:

```python
from azure.ai.projects import AIProjectClient

client = AIProjectClient(endpoint=..., credential=...)
# Use client.evaluations to run evaluation flows against the Skill
# See: https://learn.microsoft.com/en-us/azure/foundry/ai-services/evaluation/
```
