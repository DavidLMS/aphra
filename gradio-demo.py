import gradio as gr
from aphra import translate
import toml
import tempfile
import os

theme = gr.themes.Soft(
    primary_hue="rose",
    secondary_hue="pink",
    spacing_size="lg",
)

def create_config_file(api_key, writer_model, searcher_model, critic_model):
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
        os.unlink(config_file)  # Eliminar el archivo temporal
    
    return translation

def create_interface():
    with gr.Blocks(theme=theme) as demo:
        gr.Markdown("# 🌐💬 Aphra")
        
        api_key = gr.Textbox(label="Openrouter API Key", type="password")
        
        writer_model = gr.Dropdown(
            ["anthropic/claude-3.5-sonnet:beta", "other_model1", "other_model2"],
            label="Writer Model",
            value="anthropic/claude-3.5-sonnet:beta"
        )
        searcher_model = gr.Dropdown(
            ["perplexity/llama-3-sonar-large-32k-online", "other_model3", "other_model4"],
            label="Searcher Model",
            value="perplexity/llama-3-sonar-large-32k-online"
        )
        critic_model = gr.Dropdown(
            ["anthropic/claude-3.5-sonnet:beta", "other_model5", "other_model6"],
            label="Critic Model",
            value="anthropic/claude-3.5-sonnet:beta"
        )
        
        source_lang = gr.Dropdown(
            ["Spanish", "English", "French", "German"],
            label="Source Language",
            value="Spanish"
        )
        target_lang = gr.Dropdown(
            ["English", "Spanish", "French", "German"],
            label="Target Language",
            value="English"
        )
        
        file = gr.File(label="Upload .txt or .md file", file_types=[".txt", ".md"])
        text_input = gr.Textbox(label="Or paste your text here", lines=5)
        
        translate_btn = gr.Button("Translate")
        
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