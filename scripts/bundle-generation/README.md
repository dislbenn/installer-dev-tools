# Bundle Generation Scripts

## move-charts.py

This Python script automates the process of generating Helm charts by cloning specified Git repositories, copying necessary files (like Chart.yaml, values.yaml, and CRD files), and organizing them into a templated Helm chart structure. It allows the generation of Helm charts from repositories, adding CRDs as needed, and organizing the output into a specific directory structure.

Key Features:
    Clones repositories: Fetches the repositories listed in a configuration file and checks out the specified branches (if any).
    Processes charts: Iterates through the charts listed in the configuration and validates chart configuration.
    Copies chart templates: Templates Helm charts from the source files, including Chart.yaml, values.yaml, and templates.
    Adds CRDs: If CRDs are defined in the chart, they are copied to the appropriate directory in the destination.
    Directory Cleanup: After the process completes, temporary directories are cleaned up.


How to Use:

    Configure your repositories: Ensure that the copy-config.yaml file is populated with the correct repository URLs, branches, and charts to process.
    Run the script: Execute the script with the following command:

    python3 scripts/bundle-generation/move-charts.py --destination <path_to_output_directory>

    This will clone the specified repositories, process the charts, and generate the output at the destination.

Example of copy-config.yaml:

The configuration file copy-config.yaml contains details about the repositories and charts to process. Here is an example structure:

- repo_name: "example-repo"
  github_ref: "https://github.com/org/repo.git"
  branch: "main"
  charts:
    - name: "chart-name"
      chart-path: "charts/chart-name"
      always-or-toggle: "always"

Requirements:

    Python 3.6+.
    Required Python modules:
        argparse
        os
        shutil
        yaml
        gitpython (installed via pip install gitpython)

sync-pipeline-sha.py

This Python script automates the process of syncing the SHA (commit hash) values of repositories listed in a configuration YAML file with those found in the latest pipeline manifest file. It clones a specified repository, fetches the most recent manifest file from the snapshots directory, and compares the SHA values. If a mismatch is found, it updates the SHA in the YAML configuration file.
Key Features:

    Clones pipeline repository: Fetches the specified GitHub repository and checks out the desired branch.
    Fetches the latest manifest: Retrieves the most recent manifest file from the repository's snapshots directory.
    Compares SHA values: Compares the SHA from the repository's configuration file with the SHA in the manifest data.
    Updates YAML: If a SHA mismatch is detected, the corresponding repository's SHA value in the YAML file is updated.
    Directory Cleanup: After processing, the script removes temporary directories used during the cloning and syncing process.

    How to Use:

    Configure your repositories: Ensure the config.yaml file contains the correct repository names and SHA values to compare against.
    Run the script: Execute the script with the following command:

    python3 scripts/bundle-generation/sync-pipeline-sha.py --org <org_name> --repo <repo_name> --branch <branch_name>

    This will clone the specified repository, check for SHA mismatches in the pipeline manifest, and update the YAML configuration file accordingly.

Example of config.yaml:

The config.yaml file contains repository configurations, including the repository name and SHA value. Here is an example structure:

- repo_name: "example-repo"
  sha: "1234567890abcdef"

Requirements:

    Python 3.6+.
    Required Python modules:
        argparse
        coloredlogs
        glob
        json
        yaml
        gitpython (install via pip install gitpython)

generate-charts.py

This Python script automates the process of generating Helm charts from GitHub repositories specified in a configuration file (charts-config.yaml). The script clones the repositories, applies any necessary overrides, and creates Helm charts from the defined operator charts within each repository.
Key Features:

    Clones Repositories: Fetches specified repositories from GitHub, optionally checking out a specified branch.
    Generates Helm Charts: Creates Helm charts from operator chart configurations.
    Applies Overrides: Allows for the inclusion of custom Helm overrides for charts, including image mappings and RBAC adjustments.
    Lints Helm Charts: Optionally lints Helm charts to ensure they are valid before applying overrides or generating the charts.
    Handles CRDs: Copies CRDs (Custom Resource Definitions) into the destination Helm chart directory.
    Configurable Behavior: Provides various flags to control the script's behavior, such as whether to apply overrides or whether to only lint charts.

Directory Structure:

scripts/
├── aks
│   ├── README.md           # Overview of AKS-related scripts
│   ├── create-aks.sh       # Script to create AKS clusters
│   └── delete-aks.sh       # Script to delete AKS clusters
├── bundle-generation
│   ├── bundles-to-charts.py  # Convert bundles to Helm charts
│   ├── generate-charts.py    # Script to generate Helm charts from repositories
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

    Configure your charts: Ensure the charts-config.yaml file is set up correctly with repository and chart information. This file should include GitHub references, chart names, and other configuration details.
    Run the script: Execute the script using the following command:

    python3 scripts/bundle-generation/generate-charts.py --destination <destination_path> --skipOverrides <skip_overrides_flag> --lint <lint_flag>

        --destination (required): Path where the Helm charts will be created.
        --skipOverrides (optional): If set to true, Helm flow control overrides will be skipped.
        --lint (optional): If set to true, the script will only lint the charts and ensure they can be transformed without generating them.

Example of charts-config.yaml:

The charts-config.yaml file holds the configuration for repositories and charts. Here is an example structure:

- repo_name: "example-repo"
  github_ref: "https://github.com/org/example-repo.git"
  branch: "main"
  charts:
    - name: "chart1"
      always-or-toggle: "always"
      updateChartVersion: true
      imageMappings: 
        "image1": "new-image-ref"
      exclusions:
        - "exclusion1"
      inclusions:
        - "inclusion1"

Requirements:

    Python 3.6+.
    Required Python modules:
        argparse
        yaml
        gitpython (install via pip install gitpython)
        shutil
        logging

bundles-to-charts.py

This Python script automates the process of converting Operator bundles into Helm charts. It retrieves the bundle manifests either from a GitHub repository or by running a bundle generation tool, then creates Helm charts based on these manifests.
Key Features:

    GitHub Repository Input: Supports cloning GitHub repositories that contain operator bundles, extracting operator-specific data.
    Bundle Generation Tool: Supports invoking an external bundle generation tool if bundle input is not available in a GitHub repository.
    CSV Validation: Optionally validates the Operator's CSV (ClusterServiceVersion) before generating Helm charts, ensuring that the bundle's resources are correct.
    Generates Helm Charts: Converts bundles into Helm charts by creating templates and filling in necessary configuration files like Chart.yaml and resources from the CSV.
    Applies Overrides: Includes functionality for injecting overrides into Helm charts (e.g., image mappings, exclusions).
    Preserves Files: Optionally preserves specified files in the generated Helm charts.

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

    Configure your bundles: Ensure the config.yaml file is set up correctly with repository and bundle details. The file should include either a github_ref (GitHub repository) or a gen_command (bundle generation command), along with operator-specific properties.
    Run the script: Execute the script using the following command:

    python3 scripts/bundle-generation/bundles-to-charts.py --destination <destination_path> --skipOverrides <skip_overrides_flag> --lint <lint_flag>

        --destination (required): Path where the Helm charts will be created.
        --skipOverrides (optional): If set to true, Helm flow control overrides will be skipped.
        --lint (optional): If set to true, the script will only lint the bundles and ensure they can be transformed into charts without generating them.

Example of config.yaml:

The config.yaml file holds the configuration for repositories and bundles. Here is an example structure:

- repo_name: "example-repo"
  github_ref: "https://github.com/org/example-repo.git"
  branch: "main"
  operators:
    - name: "operator1"
      imageMappings: 
        "image1": "new-image-ref"
      exclusions:
        - "exclusion1"
      preserve_files:
        - "file1"

Requirements:

    Python 3.6+.
    Required Python modules:
        argparse
        yaml
        gitpython (install via pip install gitpython)
        shutil
        logging