"""
Context management for translation workflows.

This module provides the TranslationContext class that encapsulates
all the state and configuration needed during translation execution.
"""

from dataclasses import dataclass
from typing import Dict, Any
from .llm_client import LLMModelClient


@dataclass
class TranslationContext:
    """
    Context for translation containing parameters and settings.

    This class encapsulates the parameters and settings needed for performing a translation,
    including the model client, source and target languages, and logging preferences.
    """
    model_client: LLMModelClient
    source_language: str
    target_language: str
    log_calls: bool

    # Additional fields for workflow state
    metadata: Dict[str, Any] = None
    intermediate_results: Dict[str, Any] = None

    def __post_init__(self):
        """Initialize optional fields if not provided."""
        if self.metadata is None:
            self.metadata = {}
        if self.intermediate_results is None:
            self.intermediate_results = {}

    def get_models(self) -> Dict[str, str]:
        """Get the configured LLM models."""
        return self.model_client.llms

    def store_result(self, step_name: str, result: Any) -> None:
        """Store intermediate result from a workflow step."""
        self.intermediate_results[step_name] = result

    def get_result(self, step_name: str) -> Any:
        """Retrieve intermediate result from a workflow step."""
        return self.intermediate_results.get(step_name)
