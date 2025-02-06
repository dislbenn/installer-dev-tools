#!/usr/bin/env python3
# Copyright (c) 2021 Red Hat, Inc.
# Copyright Contributors to the Open Cluster Management project
# Assumes: Python 3.6+

"""
Copy Helm Chart Generation Script

This script automates the process of generating Helm charts from multiple repositories based
on configuration data provided in `copy-config.yaml`. It performs the following tasks:

1. Clones repositories specified in `copy-config.yaml`.
2. Checks out a specific branch if defined.
3. Extracts and copies Custom Resource Definitions (CRDs) from the cloned repository.
4. Generates Helm charts by copying and templating chart configurations.
5. Saves the generated Helm charts into a destination directory.
6. Cleans up temporary files after processing.

Requirements:
- Python 3.6 or higher
- External libraries: `argparse`, `os`, `shutil`, `yaml`, `logging`, `subprocess`, `gitpython`

Usage:
    python3 copy-helm-charts.py --destination <output_directory>

Arguments:
    --destination: The directory where the generated Helm charts will be stored.

Logs are generated throughout the process to provide insights into cloning, chart generation,
and cleanup activities. The script exits with an error if an issue is encountered during processing.
"""

import argparse
import logging
import os
import shutil
import sys

import yaml

from git import Repo
from validate_csv import *

def copy_helm_chart(destination_chart_path, repo, chart):
    """_summary_

    Args:
        destination_chart_path (_type_): _description_
        repo (_type_): _description_
        chart (_type_): _description_
    """
    chart_name = chart.get("name")
    logging.info("Copying templates into new %s chart directory ...", chart_name)

    # Create main folder
    chart_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "tmp", repo, chart["chart-path"])

    if os.path.exists(destination_chart_path):
        logging.info("Removing existing directory at: %s", destination_chart_path)
        shutil.rmtree(destination_chart_path)

    # Copy Chart.yaml, values.yaml, and templates dir
    chart_templates_path = os.path.join(chart_path, "templates/")
    destination_template_dir = os.path.join(destination_chart_path, "templates/")
    os.makedirs(destination_template_dir)
    logging.debug("Created destination template directory at: %s", destination_template_dir)

    # Fetch template files
    logging.info(
        "Copying template files from '%s' to '%s'",
        chart_templates_path, destination_template_dir
    )

    for file_name in os.listdir(chart_templates_path):
        # Construct full file path
        source = os.path.join(chart_templates_path, file_name)
        destination = os.path.join(destination_template_dir, file_name)

        # Copy only files
        if os.path.isfile(source):
            logging.debug("Copying file '%s' to '%s'", source, destination)
            shutil.copyfile(source, destination)
        else:
            logging.warning("Skipping non-file item: %s", source)

    chart_yaml_path = os.path.join(chart_path, "Chart.yaml")
    if not os.path.exists(chart_yaml_path):
        logging.error("No Chart.yaml found for chart: '%s'", chart_name)
        return

    logging.info("Copying Chart.yaml to '%s'", os.path.join(destination_chart_path, "Chart.yaml"))
    shutil.copyfile(chart_yaml_path, os.path.join(destination_chart_path, "Chart.yaml"))

    values_yaml_path = os.path.join(chart_path, "values.yaml")
    if not os.path.exists(values_yaml_path):
        logging.error("No values.yaml found for chart: '%s'", chart_name)
        return

    shutil.copyfile(values_yaml_path, os.path.join(destination_chart_path, "values.yaml"))
    logging.info("Chart copied.\n")

def add_crds(repo, chart, output_dir):
    """_summary_

    Args:
        repo (_type_): _description_
        chart (_type_): _description_
        output_dir (_type_): _description_
    """
    if not 'chart-path' in chart:
        logging.critical("Could not validate chart path in given chart: %s", chart)
        sys.exit(1)

    chart_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "tmp", repo, chart["chart-path"]
    )

    if not os.path.exists(chart_path):
        logging.critical("Could not validate chartPath at given path: %s", chart_path)
        sys.exit(1)

    crd_path = os.path.join(chart_path, "crds")
    if not os.path.exists(crd_path):
        logging.info("No CRDs for repo: %s", repo)
        return

    destination_path = os.path.join(output_dir, "crds", chart['name'])
    if os.path.exists(destination_path): # If path exists, remove and re-clone
        shutil.rmtree(destination_path)
    os.makedirs(destination_path)
    for filename in os.listdir(crd_path):
        if not filename.endswith(".yaml"):
            continue
        file_path = os.path.join(crd_path, filename)
        with open(file_path, 'r', encoding="utf-8") as file:
            resource_file = yaml.safe_load(file)

        if resource_file["kind"] == "CustomResourceDefinition":
            shutil.copyfile(file_path, os.path.join(destination_path, filename))

def is_chart_config_acceptable(chart):
    """_summary_

    Args:
        chart (_type_): _description_

    Returns:
        _type_: _description_
    """
    helm_chart = chart.get("name")
    if helm_chart == "":
        logging.critical("Unable to generate helm chart without a name.")
        return False
    return True

def main():
    """_summary_
    """
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Script started.")

    ## Initialize ArgParser
    parser = argparse.ArgumentParser()
    parser.add_argument("--destination", dest="destination", type=str,
        required=False, help="Destination directory of the created helm chart")

    args = parser.parse_args()
    destination = args.destination

    # Config.yaml holds the configurations for Operator bundle locations to be used
    script_dir = os.path.dirname(os.path.realpath(__file__))
    copy_config_yaml_file_path = os.path.join(script_dir, "copy-config.yaml")
    
    logging.info("script_dir: %s", script_dir)
    logging.info("copy_config_yaml_file_path: %s", copy_config_yaml_file_path)
    exit(0)

    config_yaml = os.path.join(os.path.dirname(os.path.realpath(__file__)), "copy-config.yaml")
    with open(config_yaml, 'r', encoding="utf-8") as file:
        config = yaml.safe_load(file)

    # Loop through each repo in the config.yaml
    for repo in config:
        logging.info("Cloning: %s", repo["repo_name"])
        repo_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "tmp/" + repo["repo_name"]
        ) # Path to clone repo to

        if os.path.exists(repo_path): # If path exists, remove and re-clone
            shutil.rmtree(repo_path)

        repository = Repo.clone_from(repo["github_ref"], repo_path) # Clone repo to above path
        if 'branch' in repo:
            repository.git.checkout(repo['branch']) # If a branch is specified, checkout that branch

        # Loop through each operator in the repo identified by the config
        for chart in repo["charts"]:
            if not is_chart_config_acceptable(chart):
                logging.critical(
                    "Unable to generate helm chart without configuration requirements."
                )
                sys.exit(1)

            logging.info("Helm Chartifying -  %s!\n", chart["name"])

            logging.info("Adding CRDs -  %s!\n", chart["name"])
            # Copy over all CRDs to the destination directory
            add_crds(repo["repo_name"], chart, destination)

            logging.info("Creating helm chart: '%s' ...", chart["name"])

            always_or_toggle = chart['always-or-toggle']
            destination_chart_path = os.path.join(
                destination, "charts", always_or_toggle, chart['name'])

            # Template Helm Chart Directory from 'chart-templates'
            logging.info("Templating helm chart '%s' ...", chart["name"])
            copy_helm_chart(destination_chart_path, repo["repo_name"], chart)

    logging.info("All repositories and operators processed successfully.")
    logging.info("Performing cleanup...")
    shutil.rmtree(
        (os.path.join(os.path.dirname(os.path.realpath(__file__)), "tmp")),
        ignore_errors=True
    )

    logging.info("Cleanup completed.")
    logging.info("Script execution completed.")

if __name__ == "__main__":
    main()
