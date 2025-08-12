"""
Gradio web interface demo for Aphra translation system.

This module provides a user-friendly web interface for the Aphra translation
system using Gradio, allowing users to configure models and translate text
through a browser interface.
"""
import os
import tempfile
import gradio as gr
import toml
import requests
import logging
# Import the translate function
from aphra import translate

OPENROUTER_MODELS_URL="https://openrouter.ai/api/v1/models"

theme = gr.themes.Soft(
    primary_hue="rose",
    secondary_hue="pink",
    spacing_size="lg",
)

def fetch_openrouter_models():
    """
    Fetch available models from OpenRouter API.
    Returns a list of model IDs (names).
    """
    try:
        response = requests.get(OPENROUTER_MODELS_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Extract model IDs from the response
        models = [model['id'] for model in data.get('data', [])]
        return sorted(models)
    except requests.RequestException as e:
        logging.warning(f"Failed to fetch models from OpenRouter: {e}")
        # Fallback to default models if API fails
        return [
            "anthropic/claude-sonnet-4",
            "perplexity/sonar"
        ]

def get_default_models():
    """Get default model selections for different roles."""
    models = fetch_openrouter_models()

    # Default selections based on common good models
    writer_default = "anthropic/claude-sonnet-4"
    searcher_default = "perplexity/sonar"
    critic_default = "anthropic/claude-sonnet-4"

    # Use fallbacks if defaults not available
    if writer_default not in models and models:
        writer_default = models[0]
    if searcher_default not in models and models:
        searcher_default = models[0]
    if critic_default not in models and models:
        critic_default = models[0]

    return models, writer_default, searcher_default, critic_default

def create_config_file(api_key, writer_model, searcher_model, critic_model):
    """
    Create a temporary TOML configuration file for Aphra.
    
    Args:
        api_key: OpenRouter API key
        writer_model: Model to use for writing/translation
        searcher_model: Model to use for searching/research
        critic_model: Model to use for criticism/review
        
    Returns:
        str: Path to the temporary configuration file
    """
    config = {
        "openrouter": {"api_key": api_key},
        "llms": {
            "writer": writer_model,
            "searcher": searcher_model,
            "critiquer": critic_model
        }
    }
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.toml') as tmp:
        toml.dump(config, tmp)
    return tmp.name

def process_input(file, text_input, api_key, writer_model, searcher_model, critic_model, source_lang, target_lang):
    """
    Process translation input from either file or text input.
    
    Args:
        file: Uploaded file object (if any)
        text_input: Direct text input string
        api_key: OpenRouter API key
        writer_model: Model for writing/translation
        searcher_model: Model for searching/research  
        critic_model: Model for criticism/review
        source_lang: Source language for translation
        target_lang: Target language for translation
        
    Returns:
        str: Translated text
    """
    if file is not None:
        with open(file, 'r', encoding='utf-8') as file:
            text = file.read()
    else:
        text = text_input
    config_file = create_config_file(api_key, writer_model, searcher_model, critic_model)
    try:
        translation = translate(
            source_language=source_lang,
            target_language=target_lang,
            text=text,
            config_file=config_file,
            log_calls=False
        )
    finally:
        os.unlink(config_file)

    return translation

def create_interface():
    """
    Create and configure the Gradio web interface.
    
    Returns:
        gr.Blocks: Configured Gradio interface
    """
    # Get dynamic model list and defaults
    models, writer_default, searcher_default, critic_default = get_default_models()

    with gr.Blocks(theme=theme) as demo:
        gr.Markdown("<font size=6.5><center>🌐💬 Aphra</center></font>")
        gr.Markdown(
            """<div style="display: flex;align-items: center;justify-content: center">
            [<a href="https://davidlms.github.io/aphra/">Project Page</a>] | [<a href="https://github.com/DavidLMS/aphra">Github</a>]</div>
            """
        )
        gr.Markdown("🌐💬 Aphra is an open-source translation agent with a workflow architecture designed to enhance the quality of text translations by leveraging large language models (LLMs).")

        with gr.Row():
            api_key = gr.Textbox(label="OpenRouter API Key", type="password")

            writer_model = gr.Dropdown(
                models,
                label="Writer Model",
                value=writer_default,
                allow_custom_value=True
            )
            searcher_model = gr.Dropdown(
                models,
                label="Searcher Model",
                value=searcher_default,
                allow_custom_value=True
            )
            critic_model = gr.Dropdown(
                models,
                label="Critic Model",
                value=critic_default,
                allow_custom_value=True
            )

        with gr.Row():
            source_lang = gr.Dropdown(
                ["Spanish", "English", "French", "German"],
                label="Source Language",
                value="Spanish",
                allow_custom_value=True
            )
            target_lang = gr.Dropdown(
                ["English", "Spanish", "French", "German"],
                label="Target Language",
                value="English",
                allow_custom_value=True
            )

        with gr.Row():
            file = gr.File(label="Upload .txt or .md file", file_types=[".txt", ".md"])
            text_input = gr.Textbox(label="Or paste your text here", lines=5)

        translate_btn = gr.Button("Translate with 🌐💬 Aphra")

        output = gr.Textbox(label="Translation by 🌐💬 Aphra")

        translate_btn.click(
            process_input,
            inputs=[file, text_input, api_key, writer_model, searcher_model, critic_model, source_lang, target_lang],
            outputs=[output]
        )

    return demo

if __name__ == "__main__":
    interface = create_interface()
    interface.launch()
