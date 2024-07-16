from utils import LLMModelClient, get_prompt

def translate_post(post_content, model_client, system_prompt_file, user_prompt_file, model_name, log_call=False):
    system_prompt = get_prompt(system_prompt_file)
    user_prompt = get_prompt(user_prompt_file, post_content=post_content)

    translated_content = model_client.call_model(system_prompt, user_prompt, model_name, log_call)
    return translated_content

def main():
    model_client = LLMModelClient(api_key_file="secrets.toml")
    model_name = "openai/gpt-4o-2024-05-13"
    blog_dir = Path('blog/content')
    for post_file in blog_dir.glob('*.md'):
        with open(post_file, 'r', encoding='utf-8') as file:
            content = file.read()

        translated_content = translate_post(content, model_client, 'system_prompt.txt', 'user_prompt.txt', model_name, log_call=True)

        translated_file = post_file.with_suffix('.translated.md')
        with open(translated_file, 'w', encoding='utf-8') as file:
            file.write(translated_content)

if __name__ == '__main__':
    main()
