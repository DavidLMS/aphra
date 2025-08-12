"""
Core prompt template loading utilities.

This module provides generic prompt template loading functionality
for all workflows in the Aphra translation system.
"""

import os
from importlib import resources

def get_prompt(workflow_name: str, file_name: str, **kwargs) -> str:
    """
    Reads a prompt template from a workflow's prompts directory and formats it.

    Args:
        workflow_name: Name of the workflow (e.g., 'short_article', 'subtitles')
        file_name: Name of the prompt file (e.g., 'step1_system.txt')
        **kwargs: Optional keyword arguments to format the prompt template

    Returns:
        str: The formatted prompt content

    Raises:
        FileNotFoundError: If the prompt file doesn't exist
        KeyError: If required format parameters are missing
    """
    try:
        # Try using importlib.resources first (works in packaged installations)
        ref = resources.files('aphra.workflows') / workflow_name / 'prompts' / file_name
        with ref.open('r', encoding="utf-8") as file:
            content = file.read()
    except (AttributeError, FileNotFoundError) as exc:
        # Fallback to direct file access (works in development)
        workflows_path = os.path.dirname(os.path.dirname(__file__))  # Go up to aphra/
        file_path = os.path.join(workflows_path, 'workflows', workflow_name, 'prompts', file_name)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Prompt file not found: {file_path}") from exc

        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()

    # Format the content with provided kwargs if any
    if kwargs:
        try:
            formatted_prompt = content.format(**kwargs)
        except KeyError as exc:
            msg = f"Missing format parameter {exc} for prompt {workflow_name}/{file_name}"
            raise KeyError(msg) from exc
    else:
        formatted_prompt = content

    return formatted_prompt

def list_workflow_prompts(workflow_name: str) -> list[str]:
    """
    List all available prompt files for a workflow.

    Args:
        workflow_name: Name of the workflow

    Returns:
        list[str]: List of prompt filenames available for the workflow

    Raises:
        FileNotFoundError: If the workflow prompts directory doesn't exist
    """
    try:
        # Try using importlib.resources first
        prompts_ref = resources.files('aphra.workflows') / workflow_name / 'prompts'
        return [f.name for f in prompts_ref.iterdir() if f.is_file()]
    except (AttributeError, FileNotFoundError) as exc:
        # Fallback to direct directory access
        workflows_path = os.path.dirname(os.path.dirname(__file__))
        prompts_path = os.path.join(workflows_path, 'workflows', workflow_name, 'prompts')

        if not os.path.exists(prompts_path):
            msg = f"Workflow prompts directory not found: {prompts_path}"
            raise FileNotFoundError(msg) from exc

        return [f for f in os.listdir(prompts_path)
                if os.path.isfile(os.path.join(prompts_path, f))]
