#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# create_entra_app.sh — Create the Entra ID app registration required for
# Copilot Studio to authenticate against the Foundry Toolbox MCP endpoint.
#
# Usage:
#   chmod +x scripts/create_entra_app.sh
#   ./scripts/create_entra_app.sh
#
# Prerequisites:
#   - Azure CLI (az) installed and authenticated (az login)
#   - Permission to create app registrations in your Entra ID tenant
#
# What this script does:
#   1. Creates an Entra ID app registration named "Governance Skill - Copilot Studio"
#   2. Creates a client secret (valid 1 year)
#   3. Creates a service principal for the app
#   4. Adds the Azure AI Services (ai.azure.com) delegated permission
#   5. Grants admin consent for the permission
#   6. Prints the Client ID and Client Secret for use in Copilot Studio
#
# After running:
#   - Use the printed Client ID and Client Secret in the Copilot Studio
#     MCP server OAuth configuration (see copilot_no_code/README_DEPLOY_COPILOT_GUI.md)
#   - After Copilot Studio generates a Redirect URL, run:
#     az ad app update --id <client-id> --web-redirect-uris "<redirect-url>"
# ---------------------------------------------------------------------------
set -euo pipefail

APP_NAME="Governance Skill - Copilot Studio"
# Azure AI / Azure Machine Learning Services first-party app ID
AI_RESOURCE_APP_ID="18a66f5f-dbdf-4c17-9dd7-1634712a9cbe"

echo "=== Creating Entra ID App Registration ==="
echo ""

# 1. Create the app registration
echo "1) Creating app registration: ${APP_NAME}"
APP_JSON=$(az ad app create \
  --display-name "${APP_NAME}" \
  --sign-in-audience AzureADMyOrg \
  --query "{appId:appId, objectId:id}" \
  -o json)

APP_ID=$(echo "$APP_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['appId'])")
echo "   App ID (Client ID): ${APP_ID}"

# 2. Create a client secret
echo ""
echo "2) Creating client secret (valid 1 year)"
SECRET_JSON=$(az ad app credential reset \
  --id "${APP_ID}" \
  --display-name "CopilotStudio" \
  --years 1 \
  --query "{secret:password}" \
  -o json)

CLIENT_SECRET=$(echo "$SECRET_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['secret'])")

# 3. Create a service principal
echo ""
echo "3) Creating service principal"
az ad sp create --id "${APP_ID}" -o none 2>/dev/null || true

# 4. Get the delegated permission ID for user_impersonation
echo ""
echo "4) Adding Azure AI Services (ai.azure.com) API permission"
PERM_ID=$(az ad sp show \
  --id "${AI_RESOURCE_APP_ID}" \
  --query "oauth2PermissionScopes[?value=='user_impersonation'].id | [0]" \
  -o tsv)

az ad app permission add \
  --id "${APP_ID}" \
  --api "${AI_RESOURCE_APP_ID}" \
  --api-permissions "${PERM_ID}=Scope" 2>/dev/null || true

# 5. Grant admin consent
echo ""
echo "5) Granting admin consent"
az ad app permission grant \
  --id "${APP_ID}" \
  --api "${AI_RESOURCE_APP_ID}" \
  --scope "user_impersonation" \
  -o none

# 6. Print results
TENANT_ID=$(az account show --query tenantId -o tsv)

echo ""
echo "============================================"
echo "  Entra App Registration — COMPLETE"
echo "============================================"
echo ""
echo "Use these values in Copilot Studio (Step 5 of README_DEPLOY_COPILOT_GUI.md):"
echo ""
echo "  Client ID:          ${APP_ID}"
echo "  Client secret:      ${CLIENT_SECRET}"
echo "  Authorization URL:  https://login.microsoftonline.com/${TENANT_ID}/oauth2/v2.0/authorize"
echo "  Token URL template: https://login.microsoftonline.com/${TENANT_ID}/oauth2/v2.0/token"
echo "  Refresh URL:        https://login.microsoftonline.com/${TENANT_ID}/oauth2/v2.0/token"
echo "  Scopes:             https://ai.azure.com/.default"
echo ""
echo "IMPORTANT: After Copilot Studio generates a Redirect URL, add it to the app:"
echo "  az ad app update --id ${APP_ID} --web-redirect-uris \"<redirect-url-from-copilot-studio>\""
echo ""
