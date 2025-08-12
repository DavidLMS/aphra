"""
Core components for the Aphra translation system.

This module contains the fundamental building blocks used across
all workflows.
"""

from .llm_client import LLMModelClient
from .parsers import parse_xml_tag, parse_multiple_xml_tags, parse_xml_tag_with_attributes
from .prompts import get_prompt, list_workflow_prompts
from .context import TranslationContext
from .workflow import AbstractWorkflow
from .registry import (
    WorkflowRegistry,
    get_registry,
    register_workflow,
    get_workflow,
    get_suitable_workflow
)

__all__ = [
    'LLMModelClient',
    'parse_xml_tag',
    'parse_multiple_xml_tags',
    'parse_xml_tag_with_attributes',
    'get_prompt',
    'list_workflow_prompts',
    'TranslationContext',
    'AbstractWorkflow',
    'WorkflowRegistry',
    'get_registry',
    'register_workflow',
    'get_workflow',
    'get_suitable_workflow'
]
