targetScope = 'resourceGroup'

@description('Azure region for any supplemental resources.')
param location string = resourceGroup().location

@description('Environment name supplied by azd.')
param environmentName string

@description('Principal ID used for optional role assignments or downstream access.')
param principalId string = ''

// Tagging resource to satisfy azd's requirement for at least one resource.
// The Foundry project, model deployment, ACR, and hosted agent are provisioned
// by azd via the azure.yaml service configuration (host: azure.ai.agent).
resource tags 'Microsoft.Resources/tags@2024-03-01' = {
  name: 'default'
  properties: {
    tags: {
      'azd-env-name': environmentName
      'azd-managed': 'true'
    }
  }
}
