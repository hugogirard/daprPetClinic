# Create an SSH key pair using Azure CLI

az sshkey create --name "mySSHKey" --resource-group "myResourceGroup"

# Create an SSH key pair using ssh-keygen

ssh-keygen -t rsa -b 4096

az aks install-cli

az aks get-credentials --resource-group myResourceGroup --name myAKSCluster

[Quickstart: Deploy an Azure Kubernetes Service (AKS) cluster using Bicep - Azure Kubernetes Service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/learn/quick-kubernetes-deploy-bicep?tabs=azure-cli)

dapr init -k

[Deploy Dapr on a Kubernetes cluster | Dapr Docs](https://docs.dapr.io/operations/hosting/kubernetes/kubernetes-deploy/#install-dapr-from-the-official-dapr-helm-chart-with-development-flag)

k get namespace

k get pod -n dapr-system

k apply -f .\namespace.yml
