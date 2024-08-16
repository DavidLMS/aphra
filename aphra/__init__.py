"""
Aphra package initializer.

This module exposes the translate function from the translate module.
"""

from .translate import translate
from . import llm_client
from . import prompts
from . import parsers

__all__ = ['translate', 'llm_client', 'prompts', 'parsers']
