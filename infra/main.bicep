targetScope = 'subscription'

@description('The location of the Managed Cluster resource.')
param location string

@description('The name of the resource group')
param rgName string

@description('The name of the Managed Cluster resource.')
param clusterName string

@description('Optional DNS prefix to use with hosted Kubernetes API server FQDN.')
param dnsPrefix string

@description('Disk size (in GB) to provision for each of the agent pool nodes. This value ranges from 0 to 1023. Specifying 0 will apply the default disk size for that agentVMSize.')
@minValue(0)
@maxValue(1023)
param osDiskSizeGB int

@description('The number of nodes for the cluster.')
@minValue(1)
@maxValue(50)
param agentCount int

@description('The size of the Virtual Machine.')
param agentVMSize string

@description('User name for the Linux Virtual Machines.')
param linuxAdminUsername string

@description('Configure all linux machines with the SSH RSA public key string. Your key should include three parts, for example \'ssh-rsa AAAAB...snip...UcyupgH azureuser@linuxvm\'')
param sshRSAPublicKey string

resource rg 'Microsoft.Resources/resourceGroups@2025-04-01' = {
  name: rgName
  location: location
}

module ask 'modules/k8s/aks.bicep' = {
  scope: rg
  params: {
    location: location
    agentCount: agentCount
    agentVMSize: agentVMSize
    clusterName: clusterName
    dnsPrefix: dnsPrefix
    linuxAdminUsername: linuxAdminUsername
    osDiskSizeGB: osDiskSizeGB
    sshRSAPublicKey: sshRSAPublicKey
  }
}

var suffix = uniqueString(rg.id)

// Service Bus
module serviceBus 'br/public:avm/res/service-bus/namespace:0.15.1' = {
  scope: rg
  params: {
    name: 'bus-${suffix}'
    disableLocalAuth: false
    publicNetworkAccess: 'Enabled'
    topics: [
      {
        name: 'invoice'
      }
    ]
  }
}
