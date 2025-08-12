#!/usr/bin/env python3
"""
Simple demo showing how to use the Short Article Workflow directly.

This example demonstrates the basic usage of the ShortArticleWorkflow
without any web interface - just pure Python code.
"""

import os
import tempfile
import toml
from ..short_article_workflow import ShortArticleWorkflow
from ....core.context import TranslationContext
from ....core.llm_client import LLMModelClient

def main():
    """
    Simple example of using the Short Article Workflow.
    """
    # Sample text to translate
    sample_text = """
    El cambio climático es uno de los desafíos más importantes de nuestro tiempo.
    Los científicos han demostrado que las actividades humanas están causando
    un calentamiento global sin precedentes, lo que está alterando los patrones
    climáticos en todo el mundo.
    """

    # Configuration - you would normally have this in a config file
    # Note: workflow-specific config (writer, searcher, etc.) is now handled
    # automatically by the workflow itself from its default.toml
    config_data = {
        "openrouter": {
            "api_key": "your-openrouter-api-key-here"  # Replace with your actual key
        }
    }

    print("🌐💬 Short Article Workflow Demo")
    print("=" * 40)

    # Check if API key is provided
    if config_data["openrouter"]["api_key"] == "your-openrouter-api-key-here":
        print("❌ Please set your OpenRouter API key in this script")
        print("   Edit the 'api_key' value in the config_data dictionary")
        return

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.toml') as tmp:
        toml.dump(config_data, tmp)
        config_file = tmp.name

    try:
        # Load the model client with the config file
        model_client = LLMModelClient(config_file)

        # Create translation context
        context = TranslationContext(
            model_client=model_client,
            source_language="Spanish",
            target_language="English",
            log_calls=True  # Enable logging to see the workflow steps
        )

        print("📝 Original text:")
        print(f"   {sample_text.strip()[:100]}...")
        print()

        print("🚀 Running Short Article Workflow...")
        print("   This will execute 5 steps: analyze → search → translate → critique → refine")
        print()

        # Create and run the workflow
        workflow = ShortArticleWorkflow()
        translation = workflow.run(context, sample_text.strip())

        print("✅ Translation completed!")
        print("=" * 40)
        print("🎯 Final translation:")
        print(f"   {translation}")

    except Exception as exc:
        print(f"❌ Error during translation: {exc}")
        print("   Make sure you have:")
        print("   1. Set a valid OpenRouter API key")
        print("   2. Internet connection for API calls")
        print("   3. Installed all required dependencies")

    finally:
        # Clean up temporary config file
        os.unlink(config_file)

if __name__ == "__main__":
    main()
