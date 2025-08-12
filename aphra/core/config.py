"""
Generic configuration management for workflows.

This module provides functions to load and merge workflow-specific configuration
with user overrides for any workflow in the system.
"""

import os
from typing import Dict, Any, Optional
import logging
import toml

def load_workflow_config(workflow_name: str,
                        global_config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load workflow configuration with user overrides.

    This generic function works for any workflow by:
    1. Loading default config from workflows/{workflow_name}/config/default.toml
    2. Applying user overrides from config.toml section [{workflow_name}]
    3. Returning the merged configuration

    Args:
        workflow_name: Name of the workflow (e.g., 'short_article', 'subtitles')
        global_config_path: Path to global config.toml file. If None, looks for
                          config.toml in the current working directory.

    Returns:
        Dict containing merged configuration values

    Example:
        config = load_workflow_config('short_article')
        writer_model = config.get('writer', 'default-model')
    """
    # Build path to workflow's default config
    # Assuming we're in aphra/core/ and want to reach aphra/workflows/
    core_dir = os.path.dirname(__file__)
    aphra_dir = os.path.dirname(core_dir)
    workflow_config_path = os.path.join(
        aphra_dir, 'workflows', workflow_name, 'config', 'default.toml'
    )

    # Load default workflow config
    config = {}
    try:
        with open(workflow_config_path, 'r', encoding='utf-8') as config_file:
            config = toml.load(config_file)
            logging.debug("Loaded default config for workflow '%s'", workflow_name)
    except FileNotFoundError:
        logging.warning("Default config not found for workflow '%s' at %s",
                       workflow_name, workflow_config_path)
        config = {}
    except Exception as exc:
        logging.error("Error loading default config for workflow '%s': %s",
                     workflow_name, exc)
        config = {}

    # Load user overrides from global config
    if global_config_path is None:
        global_config_path = 'config.toml'

    try:
        with open(global_config_path, 'r', encoding='utf-8') as config_file:
            global_config = toml.load(config_file)

        # Apply overrides from workflow-specific section
        if workflow_name in global_config:
            config.update(global_config[workflow_name])
            logging.debug("Applied user overrides for workflow '%s'", workflow_name)

    except FileNotFoundError:
        logging.debug("Global config file not found: %s", global_config_path)
        # No global config file, use defaults
    except Exception as exc:
        logging.warning("Error reading global config file %s: %s",
                       global_config_path, exc)
        # Error reading config, use defaults

    return config

def get_workflow_config_path(workflow_name: str) -> str:
    """
    Get the path to a workflow's default configuration file.

    Args:
        workflow_name: Name of the workflow

    Returns:
        str: Path to the workflow's default.toml file
    """
    core_dir = os.path.dirname(__file__)
    aphra_dir = os.path.dirname(core_dir)
    return os.path.join(aphra_dir, 'workflows', workflow_name, 'config', 'default.toml')

def workflow_has_config(workflow_name: str) -> bool:
    """
    Check if a workflow has a configuration file.

    Args:
        workflow_name: Name of the workflow

    Returns:
        bool: True if the workflow has a default.toml file
    """
    config_path = get_workflow_config_path(workflow_name)
    return os.path.isfile(config_path)
