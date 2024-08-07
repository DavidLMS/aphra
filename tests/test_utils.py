"""
Utility functions for tests.
"""

from aphra.translate import TranslationContext, load_model_client

def create_translation_context(config_file, source_language, target_language, log_calls=False):
    """
    Create a TranslationContext for testing purposes.

    :param config_file: Path to the TOML file containing the configuration.
    :param source_language: The source language of the text.
    :param target_language: The target language of the text.
    :param log_calls: Boolean indicating whether to log the call details.
    :return: An instance of TranslationContext.
    """
    model_client = load_model_client(config_file)
    return TranslationContext(model_client, source_language, target_language, log_calls)
