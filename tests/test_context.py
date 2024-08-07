"""
Test cases for the TranslationContext class in the aphra module.
"""

import unittest
from aphra.translate import TranslationContext
from aphra.llm_client import LLMModelClient

class TestTranslationContext(unittest.TestCase):
    """
    Test cases for the TranslationContext class in the aphra module.
    """

    def setUp(self):
        """
        Set up the test case with default parameters.
        """
        self.config_file = 'config.toml'
        self.model_client = LLMModelClient(self.config_file)
        self.context = TranslationContext(self.model_client, 'Spanish', 'English', log_calls=False)

    def test_context_initialization(self):
        """
        Test initializing the TranslationContext.
        """
        self.assertIsNotNone(self.context.model_client)
        self.assertEqual(self.context.source_language, 'Spanish')
        self.assertEqual(self.context.target_language, 'English')
        self.assertFalse(self.context.log_calls)

if __name__ == '__main__':
    unittest.main()
