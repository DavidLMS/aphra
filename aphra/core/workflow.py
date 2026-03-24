"""
Workflow base classes.

This module defines the contract for translation workflows.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from .context import TranslationContext
from .config import load_workflow_config
from .prompts import get_prompt as _get_prompt

class AbstractWorkflow(ABC):
    """
    Base class for translation workflows.

    A workflow orchestrates a translation process for a specific type of content
    using methods that can be overridden to customize behavior.

    Subclasses can use self.get_prompt() instead of importing get_prompt() directly.
    This method automatically injects the prompts_dir from the workflow config,
    enabling user-defined prompt overrides without modifying workflow code.
    """

    def __init__(self):
        """Initialize the workflow with default state."""
        self._prompts_dir: Optional[str] = None

    def get_prompt(self, file_name: str, **kwargs) -> str:
        """
        Load a prompt template for this workflow, with override support.

        This is a convenience wrapper around core.prompts.get_prompt() that
        automatically provides the workflow name and prompts_dir from config.

        Args:
            file_name: Name of the prompt file (e.g., 'step1_system.txt')
            **kwargs: Format placeholders for the prompt template

        Returns:
            str: The formatted prompt content
        """
        return _get_prompt(self.get_workflow_name(), file_name, prompts_dir=self._prompts_dir, **kwargs)

    @abstractmethod
    def get_workflow_name(self) -> str:
        """
        Get the unique name of this workflow.

        Returns:
            str: The workflow name identifier
        """
        raise NotImplementedError("Subclasses must implement get_workflow_name")

    @abstractmethod
    def is_suitable_for(self, text: str, **kwargs) -> bool:
        """
        Determine if this workflow is suitable for the given content.

        Args:
            text: The text content to evaluate
            **kwargs: Additional evaluation parameters

        Returns:
            bool: True if this workflow is suitable for the content
        """
        raise NotImplementedError("Subclasses must implement is_suitable_for")

    def load_config(self, global_config_path: str = None) -> Dict[str, Any]:
        """
        Load workflow-specific configuration.

        This method automatically loads the workflow's default configuration
        and applies user overrides from the global config file.

        Args:
            global_config_path: Path to global config file. If None, uses 'config.toml'

        Returns:
            Dict containing merged configuration values
        """
        return load_workflow_config(self.get_workflow_name(), global_config_path)

    def run(self, context: TranslationContext, text: str = None) -> str:
        """
        Run the complete workflow with configuration management.

        This method:
        1. Loads workflow-specific configuration
        2. Sets it in the translation context
        3. Calls the execute method

        Args:
            context: The translation context
            text: The text to translate (optional if already in context)

        Returns:
            str: The final translation result
        """
        # Load workflow configuration and set it in context
        workflow_config = self.load_config()
        context.set_workflow_config(workflow_config)

        # Store prompts_dir for use by self.get_prompt()
        self._prompts_dir = workflow_config.get('prompts_dir')

        # Get text from context if not provided
        if text is None:
            text = getattr(context, 'text', '')

        return self.execute(context, text)

    @abstractmethod
    def execute(self, context: TranslationContext, text: str) -> str:
        """
        Execute the complete workflow with the given context and text.

        Args:
            context: The translation context
            text: The text to translate

        Returns:
            str: The final translation result
        """
        raise NotImplementedError("Subclasses must implement execute")
