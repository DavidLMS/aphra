"""
Workflow base classes.

This module defines the contract for translation workflows.
"""

from abc import ABC, abstractmethod
from .context import TranslationContext


class AbstractWorkflow(ABC):
    """
    Base class for translation workflows.
    
    A workflow orchestrates a translation process for a specific type of content
    using methods that can be overridden to customize behavior.
    """
    
    @abstractmethod
    def get_workflow_name(self) -> str:
        """
        Get the unique name of this workflow.
        
        Returns:
            str: The workflow name identifier
        """
        pass
    
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
        pass
    
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
        pass