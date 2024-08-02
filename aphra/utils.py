import toml
import logging
import xml.etree.ElementTree as ET
from openai import OpenAI

# Logging configuration
logging.basicConfig(filename='model_calls.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class LLMModelClient:
    """
    A client for interacting with the OpenAI model via the OpenRouter API.
    """

    def __init__(self, config_file):
        """
        Initializes the LLMModelClient with the configuration from a file.

        :param config_file: Path to the TOML file containing the configuration.
        """
        self.load_config(config_file)
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key_openrouter
        )

    def load_config(self, config_file_path):
        """
        Loads configuration from a TOML file.

        :param config_file_path: Path to the TOML file.
        """
        try:
            with open(config_file_path, 'r') as file:
                config = toml.load(file)
            self.api_key_openrouter = config['openrouter']['api_key']
            self.models = config['llms']
        except FileNotFoundError:
            logging.error(f"File not found: {config_file_path}")
        except toml.TomlDecodeError:
            logging.error(f"Error decoding TOML file: {config_file_path}")
        except KeyError as e:
            logging.error(f"Missing key in config file: {e}")

    def call_model(self, system_prompt, user_prompt, model_name, log_call=False):
        """
        Calls the OpenAI model with the provided prompts.

        :param system_prompt: The system prompt to set the context for the model.
        :param user_prompt: The user prompt to send to the model.
        :param model_name: The name of the model to use.
        :param log_call: Boolean indicating whether to log the call details.
        :return: The model's response.
        """
        response = self.client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        response_content = response.choices[0].message.content

        if log_call:
            self.log_model_call(user_prompt, response_content)

        return response_content

    def log_model_call(self, user_prompt, response):
        """
        Logs the details of a model call to a log file.

        :param user_prompt: The user prompt sent to the model.
        :param response: The response received from the model.
        """
        logging.info("\nUSER_PROMPT\n")
        logging.info(user_prompt)
        logging.info("\nRESPONSE\n")
        logging.info(response)

def get_prompt(file_name, **kwargs):
    """
    Reads a prompt template from a file and formats it with the given arguments.

    :param file_name: Path to the file containing the prompt template.
    :param kwargs: Optional keyword arguments to format the prompt template.
    :return: The formatted prompt.
    """
    with open(file_name, 'r', encoding="utf-8") as file:
        content = file.read()
        if kwargs:
            formatted_prompt = content.format(**kwargs)
        else:
            formatted_prompt = content
    return formatted_prompt

def parse_analysis(analysis_str):
    """
    Parses the analysis part of the provided string and returns a list of items with their names and keywords.

    :param analysis_str: String containing the analysis in the specified format.
    :return: A list of dictionaries, each containing 'name' and 'keywords' from the analysis.
    """
    try:
        # Extract the <analysis> part
        analysis_start = analysis_str.index("<analysis>") + len("<analysis>")
        analysis_end = analysis_str.index("</analysis>")
        analysis_content = analysis_str[analysis_start:analysis_end].strip()

        # Parse the analysis content using XML parser
        root = ET.fromstring(f"<root>{analysis_content}</root>")
        items = []

        for item in root.findall('item'):
            name = item.find('name').text
            keywords = item.find('keywords').text
            items.append({'name': name, 'keywords': keywords.split(', ')})

        return items
    except ValueError as e:
        logging.error(f"Error parsing analysis string: {e}")
        return []
    except ET.ParseError as e:
        logging.error(f"Error parsing XML content: {e}")
        return []
    
def parse_translation(translation_str):
    """
    Parses the provided string and returns the content within <improved_translation> and <translators_notes> tags.

    :param translation_str: String containing the translation and notes in the specified format.
    :return: A tuple containing two strings: the content of <improved_translation> and <translators_notes>.
    """
    try:
        # Extract the <improved_translation> part
        improved_translation_start = translation_str.index("<improved_translation>") + len("<improved_translation>")
        improved_translation_end = translation_str.index("</improved_translation>")
        improved_translation_content = translation_str[improved_translation_start:improved_translation_end].strip()
        
        # Extract the <translators_notes> part
        translators_notes_start = translation_str.index("<translators_notes>") + len("<translators_notes>")
        translators_notes_end = translation_str.index("</translators_notes>")
        translators_notes_content = translation_str[translators_notes_start:translators_notes_end].strip()
        
        return improved_translation_content, translators_notes_content
    except ValueError as e:
        logging.error(f"Error parsing translation string: {e}")
        return "", ""
