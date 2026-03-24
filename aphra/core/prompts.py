"""
Core prompt template loading utilities.

This module provides generic prompt template loading functionality
for all workflows in the Aphra translation system.

Supports user-defined prompt overrides via the `prompts_dir` configuration option.
When a prompts_dir is set in the workflow config, prompts are resolved as follows:

    1. If `{prompts_dir}/{file_name}` exists → full override (replaces the default prompt)
    2. Otherwise, the default prompt is loaded from the package, and:
       - If `{prompts_dir}/{base}_prepend.txt` exists → its content is prepended
       - If `{prompts_dir}/{base}_append.txt` exists → its content is appended

    Where `{base}` is the file name without extension (e.g., 'step3_system' for 'step3_system.txt').

All prompt files (default, override, prepend, append) support the same {placeholder} variables.
"""

import os
import logging
from importlib import resources

logger = logging.getLogger(__name__)


def _load_default_prompt(workflow_name: str, file_name: str) -> str:
    """
    Load a prompt template from the workflow's built-in prompts directory.

    Args:
        workflow_name: Name of the workflow (e.g., 'short_article')
        file_name: Name of the prompt file (e.g., 'step1_system.txt')

    Returns:
        str: The raw prompt content

    Raises:
        FileNotFoundError: If the prompt file doesn't exist
    """
    try:
        # Try using importlib.resources first (works in packaged installations)
        ref = resources.files('aphra.workflows') / workflow_name / 'prompts' / file_name
        with ref.open('r', encoding="utf-8") as file:
            return file.read()
    except (AttributeError, FileNotFoundError) as exc:
        # Fallback to direct file access (works in development)
        workflows_path = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(workflows_path, 'workflows', workflow_name, 'prompts', file_name)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Prompt file not found: {file_path}") from exc

        with open(file_path, 'r', encoding="utf-8") as file:
            return file.read()


def _read_file_if_exists(file_path: str) -> str:
    """
    Read a file and return its content, or return None if it doesn't exist.

    Args:
        file_path: Absolute or relative path to the file

    Returns:
        str or None: File content, or None if the file doesn't exist
    """
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding="utf-8") as file:
            return file.read()
    return None


def _format_prompt(content: str, workflow_name: str, file_name: str, **kwargs) -> str:
    """
    Apply format placeholders to a prompt string.

    Args:
        content: The raw prompt content with {placeholders}
        workflow_name: Workflow name (for error messages)
        file_name: File name (for error messages)
        **kwargs: Placeholder values

    Returns:
        str: The formatted prompt
    """
    if kwargs:
        try:
            return content.format(**kwargs)
        except KeyError as exc:
            msg = f"Missing format parameter {exc} for prompt {workflow_name}/{file_name}"
            raise KeyError(msg) from exc
    return content


def get_prompt(workflow_name: str, file_name: str, prompts_dir: str = None, **kwargs) -> str:
    """
    Load a prompt template, applying user overrides if configured.

    Resolution order when prompts_dir is set:
        1. Full override: {prompts_dir}/{file_name} replaces the default entirely
        2. Extend: default prompt with optional prepend/append from:
           - {prompts_dir}/{base}_prepend.txt (added before the default)
           - {prompts_dir}/{base}_append.txt (added after the default)

    When prompts_dir is not set, the default prompt from the package is used as-is.

    All files support the same {placeholder} format variables.

    Args:
        workflow_name: Name of the workflow (e.g., 'short_article', 'subtitles')
        file_name: Name of the prompt file (e.g., 'step1_system.txt')
        prompts_dir: Optional path to a directory with prompt overrides
        **kwargs: Optional keyword arguments to format the prompt template

    Returns:
        str: The formatted prompt content

    Raises:
        FileNotFoundError: If the default prompt file doesn't exist
        KeyError: If required format parameters are missing
    """
    base_name = os.path.splitext(file_name)[0]

    if prompts_dir:
        # Check for full override
        override_path = os.path.join(prompts_dir, file_name)
        override_content = _read_file_if_exists(override_path)

        if override_content is not None:
            logger.debug("Using prompt override: %s/%s", prompts_dir, file_name)
            return _format_prompt(override_content, workflow_name, file_name, **kwargs)

        # Load default and apply prepend/append
        content = _load_default_prompt(workflow_name, file_name)

        prepend_path = os.path.join(prompts_dir, f"{base_name}_prepend.txt")
        prepend_content = _read_file_if_exists(prepend_path)
        if prepend_content is not None:
            logger.debug("Prepending to prompt: %s/%s_prepend.txt", prompts_dir, base_name)
            content = prepend_content + "\n\n" + content

        append_path = os.path.join(prompts_dir, f"{base_name}_append.txt")
        append_content = _read_file_if_exists(append_path)
        if append_content is not None:
            logger.debug("Appending to prompt: %s/%s_append.txt", prompts_dir, base_name)
            content = content + "\n\n" + append_content

        return _format_prompt(content, workflow_name, file_name, **kwargs)

    # No overrides — load default prompt
    content = _load_default_prompt(workflow_name, file_name)
    return _format_prompt(content, workflow_name, file_name, **kwargs)


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
