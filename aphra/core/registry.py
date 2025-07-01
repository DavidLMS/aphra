"""
Workflow registry for managing available translation workflows.

This module provides a centralized registry for discovering and
managing translation workflows.
"""

from typing import Dict, List, Optional, Type
from .workflow import AbstractWorkflow
from ..workflows import ArticleWorkflow


class WorkflowRegistry:
    """
    Registry for managing translation workflows.

    This class maintains a registry of available workflows and provides
    methods for workflow discovery and selection.
    """

    def __init__(self):
        """Initialize the workflow registry with default workflows."""
        self._workflows: Dict[str, Type[AbstractWorkflow]] = {}
        self._register_default_workflows()

    def _register_default_workflows(self):
        """Register the default workflows that come with Aphra."""
        self.register_workflow(ArticleWorkflow)

    def register_workflow(self, workflow_class: Type[AbstractWorkflow]):
        """
        Register a new workflow type.

        Args:
            workflow_class: The workflow class to register
        """
        # Create temporary instance to get the workflow name
        temp_workflow = workflow_class()
        workflow_name = temp_workflow.get_workflow_name()
        self._workflows[workflow_name] = workflow_class

    def get_workflow(self, workflow_name: str) -> Optional[AbstractWorkflow]:
        """
        Get a workflow instance by name.

        Args:
            workflow_name: The name of the workflow to retrieve

        Returns:
            AbstractWorkflow: An instance of the requested workflow, or None if not found
        """
        workflow_class = self._workflows.get(workflow_name)
        if workflow_class:
            return workflow_class()
        return None

    def get_suitable_workflow(self, text: str, **kwargs) -> Optional[AbstractWorkflow]:
        """
        Find the most suitable workflow for the given content.

        Args:
            text: The text content to analyze
            **kwargs: Additional parameters for workflow evaluation

        Returns:
            AbstractWorkflow: The most suitable workflow instance, or None if none found
        """
        # For now, we check workflows in registration order
        # In the future, we could implement more sophisticated selection logic
        for workflow_class in self._workflows.values():
            workflow = workflow_class()
            if workflow.is_suitable_for(text, **kwargs):
                return workflow

        return None

    def list_workflows(self) -> List[str]:
        """
        Get a list of all registered workflow names.

        Returns:
            List[str]: Names of all registered workflows
        """
        return list(self._workflows.keys())

    def get_workflow_info(self, workflow_name: str) -> Optional[Dict[str, str]]:
        """
        Get information about a specific workflow.

        Args:
            workflow_name: The name of the workflow

        Returns:
            Dict[str, str]: Information about the workflow, or None if not found
        """
        workflow = self.get_workflow(workflow_name)
        if workflow:
            return {
                'name': workflow.get_workflow_name(),
                'class': workflow.__class__.__name__,
                'module': workflow.__class__.__module__
            }
        return None


# Global registry instance
_registry = WorkflowRegistry()


def get_registry() -> WorkflowRegistry:
    """
    Get the global workflow registry instance.

    Returns:
        WorkflowRegistry: The global registry instance
    """
    return _registry


def register_workflow(workflow_class: Type[AbstractWorkflow]):
    """
    Convenient function to register a workflow with the global registry.

    Args:
        workflow_class: The workflow class to register
    """
    _registry.register_workflow(workflow_class)


def get_workflow(workflow_name: str) -> Optional[AbstractWorkflow]:
    """
    Convenient function to get a workflow from the global registry.

    Args:
        workflow_name: The name of the workflow to retrieve

    Returns:
        AbstractWorkflow: An instance of the requested workflow, or None if not found
    """
    return _registry.get_workflow(workflow_name)


def get_suitable_workflow(text: str, **kwargs) -> Optional[AbstractWorkflow]:
    """
    Convenient function to find a suitable workflow from the global registry.

    Args:
        text: The text content to analyze
        **kwargs: Additional parameters for workflow evaluation

    Returns:
        AbstractWorkflow: The most suitable workflow instance, or None if none found
    """
    return _registry.get_suitable_workflow(text, **kwargs)
