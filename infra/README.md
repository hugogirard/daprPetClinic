# Create an SSH key pair using Azure CLI

az sshkey create --name "mySSHKey" --resource-group "myResourceGroup"

# Create an SSH key pair using ssh-keygen

ssh-keygen -t rsa -b 4096
