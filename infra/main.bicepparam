using 'main.bicep'

param dnsPrefix = 'aks101'

param linuxAdminUsername = ''

param location = 'canadacentral'

param rgName = 'rg-dapr-demo'

param sshRSAPublicKey = ''

param agentCount = 3

param agentVMSize = 'standard_d2s_v3'

param osDiskSizeGB = 0

param clusterName = 'aks101cluster'
