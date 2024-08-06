from .utils import LLMModelClient, get_prompt, parse_analysis, parse_translation

def load_model_client(config_file):
    return LLMModelClient(config_file)

def call_model(model_client, system_file, user_file, model_name, log_calls, **kwargs):
    system_prompt = get_prompt(system_file, **kwargs)
    user_prompt = get_prompt(user_file, **kwargs)
    return model_client.call_model(system_prompt, user_prompt, model_name, log_call=log_calls)

def generate_glossary(model_client, parsed_items, source_language, target_language, model_searcher, log_calls):
    glossary = []
    for item in parsed_items:
        term_explanation = call_model(
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
    model_client = load_model_client(config_file)
    models = model_client.llms

    analysis_content = call_model(
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

    translated_content = call_model(
        model_client,
        'step3_system.txt',
        'step3_user.txt',
        models['writer'],
        log_calls,
        text=text,
        source_language=source_language,
        target_language=target_language
    )

    critique = call_model(
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

    final_translation_content = call_model(
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