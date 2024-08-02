from pathlib import Path
from .utils import LLMModelClient, get_prompt, parse_analysis, parse_translation

def translate(source_language, target_language, text):
    config_file = "config.toml"
    model_client = LLMModelClient(config_file)

    model_writer = model_client.llms['writer']
    model_searcher = model_client.llms['searcher']
    model_critiquer = model_client.llms['critiquer']

    system_prompt = get_prompt('aphra/prompts/step1_system.txt', source_language=source_language, target_language=target_language)
    user_prompt = get_prompt('aphra/prompts/step1_user.txt', post_content=text, source_language=source_language, target_language=target_language)
    analysis_content = model_client.call_model(system_prompt, user_prompt, model_writer, log_call=True)

    parsed_items = parse_analysis(analysis_content)
    
    glossary = []

    for item in parsed_items:
        system_prompt = get_prompt('aphra/prompts/step2_system.txt', source_language=source_language, target_language=target_language)
        user_prompt = get_prompt('aphra/prompts/step2_user.txt', term=item['name'], keywords=", ".join(item['keywords']), source_language=source_language)
        term_explanation = model_client.call_model(system_prompt, user_prompt, model_searcher, log_call=True)
        
        glossary_entry = f"### {item['name']}\n\n**Keywords:** {', '.join(item['keywords'])}\n\n**Explanation:**\n{term_explanation}\n"
        glossary.append(glossary_entry)

    glossary_content = "\n".join(glossary)

    system_prompt = get_prompt('aphra/prompts/step3_system.txt', source_language=source_language, target_language=target_language)
    user_prompt = get_prompt('aphra/prompts/step3_user.txt', text=text, source_language=source_language, target_language=target_language)
    translated_content = model_client.call_model(system_prompt, user_prompt, model_writer, log_call=True)
    
    system_prompt = get_prompt('aphra/prompts/step4_system.txt', source_language=source_language, target_language=target_language)
    user_prompt = get_prompt('aphra/prompts/step4_user.txt', text=text, translation=translated_content, glossary=glossary_content, source_language=source_language, target_language=target_language)
    critique = model_client.call_model(system_prompt, user_prompt, model_critiquer, log_call=True)
    
    system_prompt = get_prompt('aphra/prompts/step5_system.txt', source_language=source_language, target_language=target_language)
    user_prompt = get_prompt('aphra/prompts/step5_user.txt', text=text, translation=translated_content, glossary=glossary_content, critique=critique, source_language=source_language, target_language=target_language)
    translated_content = model_client.call_model(system_prompt, user_prompt, model_writer, log_call=True)
    
    improved_translation, translators_notes = parse_translation(translated_content)

    return improved_translation, translators_notes
