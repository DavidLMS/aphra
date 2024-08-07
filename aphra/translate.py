from .llm_client import LLMModelClient
from .prompts import get_prompt
from .parsers import parse_analysis, parse_translation

def load_model_client(config_file):
    """
    Loads the LLMModelClient with the provided configuration file.

    :param config_file: Path to the TOML file containing the configuration.
    :return: An instance of LLMModelClient initialized with the provided configuration.
    """
    return LLMModelClient(config_file)

def execute_model_call(model_client, system_file, user_file, model_name, log_calls, **kwargs):
    """
    Executes a model call using the provided system and user prompts.

    :param model_client: An instance of LLMModelClient.
    :param system_file: Path to the file containing the system prompt.
    :param user_file: Path to the file containing the user prompt.
    :param model_name: The name of the model to use.
    :param log_calls: Boolean indicating whether to log the call details.
    :param kwargs: Optional keyword arguments to format the prompt templates.
    :return: The model's response content.
    """
    system_prompt = get_prompt(system_file, **kwargs)
    user_prompt = get_prompt(user_file, **kwargs)
    return model_client.call_model(system_prompt, user_prompt, model_name, log_call=log_calls)

def generate_glossary(model_client, parsed_items, source_language, target_language, model_searcher, log_calls):
    """
    Generates a glossary of terms based on the parsed analysis items.

    :param model_client: An instance of LLMModelClient.
    :param parsed_items: A list of dictionaries containing 'name' and 'keywords' for each item.
    :param source_language: The source language of the text.
    :param target_language: The target language of the text.
    :param model_searcher: The name of the model to use for searching term explanations.
    :param log_calls: Boolean indicating whether to log the call details.
    :return: A formatted string containing the glossary entries.
    """
    glossary = []
    for item in parsed_items:
        term_explanation = execute_model_call(
            model_client,
            'step2_system.txt',
            'step2_user.txt',
            model_searcher,
            log_calls,
            term=item['name'],
            keywords=", ".join(item['keywords']),
            source_language=source_language,
            target_language=target_language
        )
        glossary_entry = f"### {item['name']}\n\n**Keywords:** {', '.join(item['keywords'])}\n\n**Explanation:**\n{term_explanation}\n"
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

    analysis_content = execute_model_call(
        model_client,
        'step1_system.txt',
        'step1_user.txt',
        models['writer'],
        log_calls,
        post_content=text,
        source_language=source_language,
        target_language=target_language
    )

    parsed_items = parse_analysis(analysis_content)
    glossary_content = generate_glossary(model_client, parsed_items, source_language, target_language, models['searcher'], log_calls)

    translated_content = execute_model_call(
        model_client,
        'step3_system.txt',
        'step3_user.txt',
        models['writer'],
        log_calls,
        text=text,
        source_language=source_language,
        target_language=target_language
    )

    critique = execute_model_call(
        model_client,
        'step4_system.txt',
        'step4_user.txt',
        models['critiquer'],
        log_calls,
        text=text,
        translation=translated_content,
        glossary=glossary_content,
        source_language=source_language,
        target_language=target_language
    )

    final_translation_content = execute_model_call(
        model_client,
        'step5_system.txt',
        'step5_user.txt',
        models['writer'],
        log_calls,
        text=text,
        translation=translated_content,
        glossary=glossary_content,
        critique=critique,
        source_language=source_language,
        target_language=target_language
    )

    improved_translation = parse_translation(final_translation_content)

    return improved_translation