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
    tags: {
      SecurityControl: 'Ignore'
    }
    disableLocalAuth: false
    publicNetworkAccess: 'Enabled'
    topics: [
      {
        name: 'invoice'
      }
    ]
  }
}

module storageAccount 'br/public:avm/res/storage/storage-account:0.29.0' = {
  scope: rg
  params: {
    name: 'str${replace(suffix,'-','')}'
    location: location
    tags: {
      SecurityControl: 'Ignore'
    }
    kind: 'StorageV2'
    publicNetworkAccess: 'Enabled'
    networkAcls: {
      ipRules: []
    }
    allowSharedKeyAccess: true
    tableServices: {
      tables: [
        {
          name: 'daprstate'
        }
      ]
    }
  }
}

module containerRegistry 'br/public:avm/res/container-registry/registry:0.9.3' = {
  scope: rg
  params: {
    tags: {
      SecurityControl: 'Ignore'
    }
    #disable-next-line BCP334
    name: 'acr${replace(suffix,'-','')}'
    location: location
    acrAdminUserEnabled: true
    publicNetworkAccess: 'Enabled'
    acrSku: 'Standard'
  }
}

module flexibleServer 'br/public:avm/res/db-for-postgre-sql/flexible-server:0.15.0' = {
  scope: rg
  params: {
    tags: {
      SecurityControl: 'Ignore'
    }
    // Required parameters
    availabilityZone: 1
    name: 'db-${suffix}'
    skuName: 'Standard_D2s_v3'
    tier: 'GeneralPurpose'
    backupRetentionDays: 20
    configurations: [
      {
        name: 'log_min_messages'
        source: 'user-override'
        value: 'INFO'
      }
    ]
    databases: [
      {
        name: 'daprstate'
      }
    ]
    firewallRules: [
      {
        endIpAddress: '0.0.0.0'
        name: 'AllowAllWindowsAzureIps'
        startIpAddress: '0.0.0.0'
      }
    ]
    geoRedundantBackup: 'Disabled'
    highAvailability: 'SameZone'
    location: location
    publicNetworkAccess: 'Enabled'
    storageSizeGB: 1024
    version: '14'
  }
}
