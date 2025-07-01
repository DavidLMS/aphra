"""
Module for translating text using multiple steps and language models.

This module provides the main translation functionality using Aphra's
workflow-based translation system.
"""

from .core.llm_client import LLMModelClient
from .core.context import TranslationContext
from .core.registry import get_suitable_workflow


def load_model_client(config_file):
    """
    Loads the LLMModelClient with the provided configuration file.

    :param config_file: Path to the TOML file containing the configuration.
    :return: An instance of LLMModelClient initialized with the provided configuration.
    """
    return LLMModelClient(config_file)


def translate(source_language, target_language, text, config_file="config.toml", log_calls=False):
    """
    Translates the provided text from the source language to the target language using workflows.

    This function provides a convenient interface to Aphra's workflow-based
    translation system.

    :param source_language: The source language of the text.
    :param target_language: The target language of the text.
    :param text: The text to be translated.
    :param config_file: Path to the TOML file containing the configuration.
    :param log_calls: Boolean indicating whether to log the call details.
    :return: The improved translation of the text.
    """
    # Load the model client
    model_client = load_model_client(config_file)

    # Create translation context
    context = TranslationContext(
        model_client=model_client,
        source_language=source_language,
        target_language=target_language,
        log_calls=log_calls
    )

    # Find the most suitable workflow for this content
    workflow = get_suitable_workflow(text)

    if workflow is None:
        raise ValueError("No suitable workflow found for the provided text")

    # Execute the workflow
    result = workflow.execute(context, text)

    return result

