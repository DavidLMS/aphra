from pathlib import Path
from utils import LLMModelClient, get_prompt, parse_analysis, parse_translation

def main():
    model_client = LLMModelClient(api_key_file="secrets.toml")
    model_name = "anthropic/claude-3.5-sonnet:beta"
    blog_dir = Path("/Users/david/Documents/GitHub/aphra/src")
    for post_file in blog_dir.glob('*.md'):
        with open(post_file, 'r', encoding='utf-8') as file:
            content = file.read()

        system_prompt = get_prompt('step1_system.txt', source_language='Spanish', target_language='English')
        user_prompt = get_prompt('step1_user.txt', post_content=content, source_language='Spanish', target_language='English')
        analysis_content = model_client.call_model(system_prompt, user_prompt, model_name, log_call=True)

        parsed_items = parse_analysis(analysis_content)
        
        glossary = []

        for item in parsed_items:
            system_prompt = get_prompt('step2_system.txt', source_language='Spanish', target_language='English')
            user_prompt = get_prompt('step2_user.txt', term=item['name'], keywords=", ".join(item['keywords']), source_language='Spanish')
            term_explanation = model_client.call_model(system_prompt, user_prompt, 'perplexity/llama-3-sonar-large-32k-online', log_call=True)
            
            glossary_entry = f"### {item['name']}\n\n**Keywords:** {', '.join(item['keywords'])}\n\n**Explanation:**\n{term_explanation}\n"
            glossary.append(glossary_entry)

        # Join all entries into a single string
        glossary_content = "\n".join(glossary)

        # Save glossary content to a file
        with open('glossary.md', 'w', encoding='utf-8') as file:
            file.write(glossary_content)

        system_prompt = get_prompt('step3_system.txt', source_language='Spanish', target_language='English')
        user_prompt = get_prompt('step3_user.txt', text=content, source_language='Spanish', target_language='English')
        translated_content = model_client.call_model(system_prompt, user_prompt, 'anthropic/claude-3.5-sonnet:beta', log_call=True)

        translated_file = post_file.with_suffix('.basic_translated.md')
        with open(translated_file, 'w', encoding='utf-8') as file:
            file.write(translated_content)
        
        system_prompt = get_prompt('step4_system.txt', source_language='Spanish', target_language='English')
        user_prompt = get_prompt('step4_user.txt', text=content, translation=translated_content, glossary=glossary_content, source_language='Spanish', target_language='English')
        critique = model_client.call_model(system_prompt, user_prompt, 'anthropic/claude-3.5-sonnet:beta', log_call=True)

        critique_file = post_file.with_suffix('.critique.md')
        with open(critique_file, 'w', encoding='utf-8') as file:
            file.write(critique)

        system_prompt = get_prompt('step5_system.txt', source_language='Spanish', target_language='English')
        user_prompt = get_prompt('step5_user.txt', text=content, translation=translated_content, glossary=glossary_content, critique=critique, source_language='Spanish', target_language='English')
        translated_content = model_client.call_model(system_prompt, user_prompt, 'anthropic/claude-3.5-sonnet:beta', log_call=True)
        
        improved_translation, translators_notes = parse_translation(translated_content)

        translated_file = post_file.with_suffix('.translated.md')
        with open(translated_file, 'w', encoding='utf-8') as file:
            file.write(improved_translation)
            file.write("\n\n")
            file.write(translators_notes)

if __name__ == '__main__':
    main()
