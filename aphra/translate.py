"""
Module for translating text using multiple steps and language models.
"""

from dataclasses import dataclass
from .llm_client import LLMModelClient
from .prompts import get_prompt
from .parsers import parse_analysis, parse_translation

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

def load_model_client(config_file):
    """
    Loads the LLMModelClient with the provided configuration file.

    :param config_file: Path to the TOML file containing the configuration.
    :return: An instance of LLMModelClient initialized with the provided configuration.
    """
    return LLMModelClient(config_file)

def execute_model_call(context, system_file, user_file, model_name, **kwargs):
    """
    Executes a model call using the provided system and user prompts.

    :param context: An instance of TranslationContext containing translation parameters.
    :param system_file: Path to the file containing the system prompt.
    :param user_file: Path to the file containing the user prompt.
    :param model_name: The name of the model to use.
    :param kwargs: Optional keyword arguments to format the prompt templates.
    :return: The model's response content.
    """
    system_prompt = get_prompt(system_file, **kwargs)
    user_prompt = get_prompt(user_file, **kwargs)
    return context.model_client.call_model(system_prompt, user_prompt, model_name, log_call=context.log_calls)

def generate_glossary(context, parsed_items, model_searcher):
    """
    Generates a glossary of terms based on the parsed analysis items.

    :param context: An instance of TranslationContext containing translation parameters.
    :param parsed_items: A list of dictionaries containing 'name' and 'keywords' for each item.
    :param model_searcher: The name of the model to use for searching term explanations.
    :return: A formatted string containing the glossary entries.
    """
    glossary = []
    for item in parsed_items:
        term_explanation = execute_model_call(
            context,
            'step2_system.txt',
            'step2_user.txt',
            model_searcher,
            term=item['name'],
            keywords=", ".join(item['keywords']),
            source_language=context.source_language,
            target_language=context.target_language
        )
        glossary_entry = (
            f"### {item['name']}\n\n**Keywords:** {', '.join(item['keywords'])}\n\n"
            f"**Explanation:**\n{term_explanation}\n"
        )
        glossary.append(glossary_entry)
    return "\n".join(glossary)

def translate(source_language, target_language, text, config_file="config.toml", log_calls=False):
    """
    Translates the provided text from the source language to the target language in multiple steps.

    :param source_language: The source language of the text.
    :param target_language: The target language of the text.
    :param text: The text to be translated.
    :param config_file: Path to the TOML file containing the configuration.
    :param log_calls: Boolean indicating whether to log the call details.
    :return: The improved translation of the text.
    """
    model_client = load_model_client(config_file)
    models = model_client.llms
    context = TranslationContext(model_client, source_language, target_language, log_calls)

    analysis_content = execute_model_call(
        context,
        'step1_system.txt',
        'step1_user.txt',
        models['writer'],
        post_content=text,
        source_language=source_language,
        target_language=target_language
    )

    parsed_items = parse_analysis(analysis_content)
    glossary_content = generate_glossary(
        context, parsed_items, models['searcher']
    )

    translated_content = execute_model_call(
        context,
        'step3_system.txt',
        'step3_user.txt',
        models['writer'],
        text=text,
        source_language=source_language,
        target_language=target_language
    )

    critique = execute_model_call(
        context,
        'step4_system.txt',
        'step4_user.txt',
        models['critiquer'],
        text=text,
        translation=translated_content,
        glossary=glossary_content,
        source_language=source_language,
        target_language=target_language
    )

    final_translation_content = execute_model_call(
        context,
        'step5_system.txt',
        'step5_user.txt',
        models['writer'],
        text=text,
        translation=translated_content,
        glossary=glossary_content,
        critique=critique,
        source_language=source_language,
        target_language=target_language
    )

    improved_translation = parse_translation(final_translation_content)

    return improved_translation
