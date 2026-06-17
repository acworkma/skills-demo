targetScope = 'resourceGroup'

@description('Azure region for any supplemental resources.')
param location string = resourceGroup().location

@description('Environment name supplied by azd.')
param environmentName string

@description('Principal ID used for optional role assignments or downstream access.')
param principalId string = ''

/*
  This Bicep file is intentionally minimal.

  In this demo, azd provisions and deploys the Azure AI Foundry agent and model
  deployment through azure.yaml service configuration. Use this template only
  for any additional infrastructure you want to add around the demo.
*/

output SERVICE_GOVERNANCE_INTAKE_AGENT_ENDPOINT string = 'set-by-azd-after-agent-deploy'
