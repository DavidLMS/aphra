import logging
import toml
import requests
from openai import OpenAI

class LLMModelClient:
    """
    A client for interacting with the model via the OpenRouter API.
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
        self.logging_configured = False

    def load_config(self, config_file_path):
        """
        Loads configuration from a TOML file.

        :param config_file_path: Path to the TOML file.
        """
        try:
            with open(config_file_path, 'r', encoding='utf-8') as file:
                config = toml.load(file)
            self.api_key_openrouter = config['openrouter']['api_key']
            self.llms = config['llms']
        except FileNotFoundError:
            logging.error('File not found: %s', config_file_path)
            raise
        except toml.TomlDecodeError:
            logging.error('Error decoding TOML file: %s', config_file_path)
            raise
        except KeyError as e:
            logging.error('Missing key in config file: %s', e)
            raise

    def call_model(self, system_prompt, user_prompt, model_name, log_call=False):
        """
        Calls the model with the provided prompts.

        :param system_prompt: The system prompt to set the context for the model.
        :param user_prompt: The user prompt to send to the model.
        :param model_name: The name of the model to use.
        :param log_call: Boolean indicating whether to log the call details.
        :return: The model's response.
        """
        try:
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
        except requests.exceptions.RequestException as e:
            logging.error('Request error: %s', e)
            raise
        except (ValueError, KeyError, TypeError) as e:
            logging.error('Error parsing response: %s', e)
            logging.error('Response content: %s', response.text if response else 'No response')
            raise

    def log_model_call(self, user_prompt, response):
        """
        Logs the details of a model call to a log file.

        :param user_prompt: The user prompt sent to the model.
        :param response: The response received from the model.
        """
        if not self.logging_configured:
            logging.basicConfig(filename='aphra.log', level=logging.INFO,
                                format='%(asctime)s - %(levelname)s - %(message)s')
            self.logging_configured = True

        logging.info("\nUSER_PROMPT\n")
        logging.info(user_prompt)
        logging.info("\nRESPONSE\n")
        logging.info(response)
      
