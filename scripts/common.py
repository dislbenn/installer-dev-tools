#!/usr/bin/env python3
# Copyright (c) 2025 Red Hat, Inc.
# Copyright Contributors to the Open Cluster Management project
# Assumes: Python 3.6+

import yaml
import os

def load_yaml(file_path):
    """Load an existing YAML file."""
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return yaml.safe_load(f) or []
    return []

def save_yaml(file_path, data):
    """Save the updated data back to the YAML file."""
    with open(file_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False)
    print(f"Updated YAML file saved to: {file_path}")