## Release

onboard-new-component.py

This Python script provides an interactive process to onboard a new repository into the configuration files for OLM (Operator Lifecycle Manager) or Helm chart automation. It collects necessary details about the repository, its components, and configuration settings, then updates a YAML configuration file with the collected information.
Key Features:

    Interactive Prompts: Uses prompts to collect required details for onboarding a new repository.
    OLM and Helm Support: The script supports two types of onboarding:
        OLM (Operator Lifecycle Manager): Adds operators with image mappings, exclusions, and bundle path details.
        Helm Charts: Adds Helm charts with details like chart path, versioning, RBAC overrides, and image mappings.
    Image Mappings: Prompts the user to provide key-value mappings for images.
    Exclusions/Inclusions: Prompts the user to select exclusions or inclusions interactively from predefined options.
    Config File Update: Updates the appropriate configuration file (either for OLM or Helm) with the new repository details.

Directory Structure:

scripts/
├── aks
│   ├── README.md           # Overview of AKS-related scripts
│   ├── create-aks.sh       # Script to create AKS clusters
│   └── delete-aks.sh       # Script to delete AKS clusters
├── bundle-generation
│   ├── bundles-to-charts.py  # Convert operator bundles to Helm charts
│   ├── generate-charts.py    # Generate Helm charts from repositories
│   ├── generate-sha-commits.py  # Generate SHA commits for repositories
│   └── move-charts.py         # Template Helm charts
├── compliance
│   ├── README.md           # Overview of compliance-related scripts
│   ├── pod-enforce.sh      # Enforce compliance via pod validation
│   └── pod-linter.sh       # Lint Kubernetes pod definitions for compliance
├── release
│   ├── README.md             # Overview of release-related scripts
│   ├── onboard-new-components.py  # Onboard new components for release
│   ├── refresh-image-alias.py    # Refresh image alias references
│   └── release-version.sh       # Release version management script
└── utils
    ├── common.py            # Common utility functions
    └── utils.py             # Additional utility functions

How to Use:

    Run the Script: To begin the onboarding process, run the script:

    python3 scripts/bundle-generation/onboard-new-component.py

    Choose Onboarding Type: The script will prompt you to choose between OLM or Helm onboarding.

    Enter Repository Details:
        Repository Name: Provide the name of the repository.
        GitHub URL: Provide the GitHub URL for the repository.
        Branch: Provide the branch name (default is main).

    Depending on the onboarding type, additional details will be prompted for:
        OLM: Operator name, bundle path, image mappings, exclusions.
        Helm: Chart name, chart path, version, RBAC settings, image mappings, inclusions.

    Add Multiple Entries: You can add multiple operators (for OLM) or charts (for Helm) in one run.

    Config File Update: The collected details will be added to the appropriate YAML configuration file (charts-config.yaml for Helm or bundle-automation/config.yaml for OLM).

Requirements:

    Python 3.6+.
    Required Python modules:
        inquirer
        utils.common (assumed to contain functions like load_yaml and save_yaml for YAML file management)

Example Configuration:

For OLM onboarding, the config file might look like this:

- repo_name: "example-repo"
  github_ref: "https://github.com/org/example-repo.git"
  branch: "main"
  operators:
    - name: "operator1"
      bundlePath: "bundles/manifests/"
      imageMappings:
        "image1": "new-image-ref"
      exclusions:
        - "readOnlyRootFilesystem"

For Helm onboarding:

- repo_name: "example-repo"
  github_ref: "https://github.com/org/example-repo.git"
  branch: "main"
  charts:
    - name: "chart1"
      chart-path: "charts/chart1/"
      always-or-toggle: "toggle"
      imageMappings:
        "image1": "new-image-ref"
      inclusions:
        - "pullSecretOverride"
      skipRBACOverrides: true
      updateChartVersion: true
      auto-install-for-all-clusters: true

refresh-image-alias.py

This Python script is designed to fetch the latest image-alias.json file from a GitHub repository containing the pipeline manifest. It clones the repository, fetches the required file, and saves it to a local directory. The script is mainly used for refreshing image alias configurations from a remote source.
Key Features:

    Clone Repository: Clones the specified repository from a GitHub organization, checking out the specified branch.
    Fetch image-alias.json: Fetches the image-alias.json file from a specific directory within the cloned repository and saves it to a local target directory.
    Directory Cleanup: Ensures that the target directory is clean by removing the existing repository directory if it already exists.
    Logging and Cleanup: Logs the process and performs cleanup after the operation is completed, removing any temporary files and directories.

Arguments:

    --org: The GitHub organization name (default: stolostron).
    --repo: The repository name from which to fetch the image-alias.json file (required).
    --branch: The branch name to clone from the repository (required).

Script Flow:

    Clone the Repository: The script uses the git module to clone the repository and checks out the specified branch.
    Fetch image-alias.json: It looks for the image-alias.json file in the cloned repository’s root or another specified path.
    Copy to Target Directory: The file is then copied into a local directory (config/images) for further use.
    Cleanup: After the operation is completed, the script deletes the temporary cloned repository and other intermediary files.

Example Usage:

To run the script, execute the following command in the terminal, passing the required arguments:

python3 refresh-image-alias.py --repo <repository-name> --branch <branch-name> --org <organization-name>

If a Personal Access Token (PAT) is required for authentication, you can either pass it as an argument or set it as an environment variable (GH_READ_PAT).
Example Execution:

python3 refresh-image-alias.py --repo "image-pipeline-repo" --branch "main" --org "stolostron"

Key Functions:

    fetch_image_alias_json(image_path):
        Copies the image-alias.json from the source repository directory to a target directory (config/images).
    clone_pipeline_repo(org, repo_name, branch, target_path, pat=None):
        Clones the repository using the GitHub URL and checks out the specified branch.
    main():
        The entry point of the script. It processes the command-line arguments, clones the repository, fetches the latest image-alias.json file, and performs cleanup.

Directory Structure:

scripts/
├── aks
│   ├── README.md           # Overview of AKS-related scripts
│   ├── create-aks.sh       # Script to create AKS clusters
│   └── delete-aks.sh       # Script to delete AKS clusters
├── bundle-generation
│   ├── bundles-to-charts.py  # Convert operator bundles to Helm charts
│   ├── generate-charts.py    # Generate Helm charts from repositories
│   ├── generate-sha-commits.py  # Generate SHA commits for repositories
│   └── move-charts.py         # Template Helm charts
├── compliance
│   ├── README.md           # Overview of compliance-related scripts
│   ├── pod-enforce.sh      # Enforce compliance via pod validation
│   └── pod-linter.sh       # Lint Kubernetes pod definitions for compliance
├── release
│   ├── README.md             # Overview of release-related scripts
│   ├── onboard-new-components.py  # Onboard new components for release
│   ├── refresh-image-alias.py    # Refresh image alias references
│   └── release-version.sh       # Release version management script
└── utils
    ├── common.py            # Common utility functions
    └── utils.py             # Additional utility functions

Example Configuration After Fetch:

Once the script completes, the image-alias.json file is saved in config/images/image-alias.json, ready for use in further automation or deployment processes.


The release-version.sh script is designed to scan OpenShift resources in the open-cluster-management and multicluster-engine namespaces to compare the release versions specified in resource annotations with the actual versions of the respective components (ACM and MCE). It checks for version mismatches and logs the results.

Here’s a breakdown of how the script works:
Overview

This script:

    Scans various resources (like deployments, roles, services, etc.) in the open-cluster-management and multicluster-engine namespaces.
    Compares the release version stored in the annotations of each resource with the actual version of the ACM and MCE components.
    Records any mismatches in a version-matches file.

Functions

    record_version_match_status:
        Records the version match status for a given resource, including whether the version in the annotation matches the component version.
        Appends the result to the version-matches file.

    clear_version_match_file:
        Clears the contents of the version-matches file before scanning begins.

    version_matches:
        Compares the two version strings. If they match, it returns "MATCH", otherwise "MISMATCH".

    scan_components:
        Defines an array of resource kinds to check, such as deployment, service, configmap, etc.
        Retrieves the version of ACM and MCE components using oc get csv and yq.
        For each resource kind, it checks both ACM and MCE resources.
        Compares the release version from resource annotations with the actual ACM and MCE component versions and records the result.

    compare_versions:
        Compares the operator version with the component version and returns true if they match, false if they don’t.

Execution Flow

    Step 1: The clear_version_match_file function clears the existing version-matches file.
    Step 2: The scan_components function iterates over the specified resource kinds (deployment, role, service, etc.).
        For each resource in the ACM and MCE namespaces, it compares the release version in the resource annotation with the actual component version (acm_version or mce_version).
        It prints the results of the version comparison.
        It records the version match or mismatch using the record_version_match_status function.

Version Comparison

    The script compares two types of version annotations for the resources:
        ACM: installer.open-cluster-management.io/release-version
        MCE: installer.multicluster.openshift.io/release-version
    It checks if the versions match between the resource and the component versions (acm_version and mce_version).

Output

    The script outputs:
        Whether the release version matches or mismatches for each resource.
        Logs the results into a version-matches file.

Example of Output

--------------------
Multicluster Engine
deployment: my-deployment
Release version mismatch. MCE: 2.3.0, Annotation: 2.2.0
--------------------
Open Cluster Management
deployment: my-deployment
Release versions match: 2.3.0

Directory Structure

scripts/
├── aks
├── bundle-generation
├── release
│   ├── onboard-new-components.py  # Onboard new components for release
│   ├── refresh-image-alias.py    # Refresh image alias references
│   ├── release-version.sh        # Release version comparison script
└── utils
    ├── common.py                 # Common utility functions
    └── utils.py                  # Additional utility functions

How to Run

You can run the script by executing:

bash release-version.sh

This will:

    Clear any existing version-matches file.
    Scan the resources in both the open-cluster-management and multicluster-engine namespaces.
    Compare the versions and print the results to the terminal.