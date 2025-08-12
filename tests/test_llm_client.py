"""
Test cases for the LLMModelClient class in the aphra module.
"""

import unittest

class TestLLMModelClient(unittest.TestCase):
    """
    Test cases for the LLMModelClient class in the aphra module.
    """

    def setUp(self):
        """
        Set up the test case with a default configuration file.
        """
        self.config_file = 'config.toml'
        from aphra.core.llm_client import LLMModelClient
        self.client = LLMModelClient(self.config_file)

    def test_load_config(self):
        """
        Test loading the configuration file.
        """
        self.assertIsNotNone(self.client.api_key_openrouter)

    def test_call_model(self):
        """
        Test making a call to the model.
        """
        system_prompt = "Translate the following text."
        user_prompt = "Hola mundo"
        model_name = "anthropic/claude-sonnet-4"
        response = self.client.call_model(system_prompt, user_prompt, model_name)
        self.assertIsNotNone(response)

if __name__ == '__main__':
    unittest.main()
