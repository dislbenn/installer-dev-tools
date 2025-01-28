# AKS

The create-aks.sh script is designed to automate the creation of an Azure Kubernetes Service (AKS) cluster, configure access to the cluster, and install the OpenShift Operator Lifecycle Manager (OLM).
Overview

The script:

    Accepts three parameters: Azure region, AKS cluster name, and resource group.
    Logs into Azure.
    Creates the resource group if it doesn't exist.
    Creates an AKS cluster with specified configurations.
    Configures the Kubernetes credentials to connect to the newly created AKS cluster.
    Installs the OpenShift OLM using the operator-sdk.

Explanation of Key Sections

    Help Function (helpFunction):
        Displays usage instructions if the script is called with missing or incorrect parameters.
        Ensures the user knows how to provide the required arguments for the script to run.

    Argument Parsing (getopts):
        The script uses getopts to parse the command line arguments. The expected arguments are:
            -r: Azure region (e.g., eastus).
            -n: Name of the AKS cluster.
            -g: Name of the Azure resource group.
        If any of the arguments are missing, the helpFunction is called.

    Validation of Parameters:
        The script checks if any of the arguments are empty and calls the help function if they are.

    Azure Authentication (az login):
        Logs into Azure using the default account or via a configured service principal.

    Resource Group Creation:
        If the specified resource group doesn't exist, it will be created in the provided Azure region.

    AKS Cluster Creation (az aks create):
        Creates an AKS cluster in the specified resource group, region, and with the specified cluster name.
        The --enable-oidc-issuer flag enables OIDC support, which is often required for integrating with other services like Red Hat OpenShift or certain identity providers.
        SSH keys are generated automatically to access the cluster.

    Kubeconfig Setup (az aks get-credentials):
        Configures your local kubectl to use the credentials for the newly created AKS cluster. This allows you to interact with the cluster immediately after it is created.

    OLM Installation (operator-sdk olm install):
        Installs OpenShift OLM on the AKS cluster to manage Kubernetes Operators.

Usage Example

To use the script, you would run the following command, providing the Azure region, AKS cluster name, and resource group:

./create-aks.sh -r eastus -n myakscluster -g myresourcegroup

This will:

    Log into Azure.
    Create a resource group named myresourcegroup in the eastus region.
    Create an AKS cluster named myakscluster in that resource group.
    Configure kubectl to use the credentials of the newly created cluster.
    Install the OpenShift OLM.

Notes

    Ensure that the az CLI is installed and authenticated in the environment where you are running the script.
    The operator-sdk should also be installed for the OLM installation command to work.


The delete-aks.sh script automates the process of deleting an existing Azure Kubernetes Service (AKS) cluster and its associated resource group in Azure.
Overview

The script:

    Accepts two parameters: the AKS cluster name and the resource group where the cluster is located.
    Logs into Azure.
    Deletes the specified AKS cluster and associated resources from Azure.

Explanation of Key Sections

    Help Function (helpFunction):
        Displays usage instructions if the script is called with missing or incorrect parameters.
        Ensures the user knows how to provide the required arguments for the script to run.

    Argument Parsing (getopts):
        The script uses getopts to parse the command line arguments. The expected arguments are:
            -n: Name of the AKS cluster.
            -g: Name of the Azure resource group where the AKS cluster is located.
        If any of the arguments are missing, the helpFunction is called.

    Validation of Parameters:
        The script checks if any of the arguments are empty and calls the help function if they are.

    Azure Authentication (az login):
        Logs into Azure using the default account or via a configured service principal.

    AKS Cluster Deletion (az aks delete):
        Deletes the AKS cluster with the specified name from the specified resource group.
        This action removes the cluster, but not necessarily the resource group itself (if the resource group contains other resources).

Usage Example

To use the script, you would run the following command, providing the name of the AKS cluster and the resource group:

./delete-aks.sh -n myakscluster -g myresourcegroup

This will:

    Log into Azure.
    Delete the AKS cluster named myakscluster in the resource group myresourcegroup.

Notes

    Ensure that the az CLI is installed and authenticated in the environment where you are running the script.
    Deleting the AKS cluster is irreversible and will result in the loss of all cluster data and configuration unless backed up.