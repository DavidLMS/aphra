"""
Test cases for the TranslationContext class in the aphra module.
"""

import unittest

class TestTranslationContext(unittest.TestCase):
    """
    Test cases for the TranslationContext class in the aphra module.
    """

    def setUp(self):
        """
        Set up the test case with default parameters.
        """
        self.config_file = 'config.toml'
        from aphra.core.llm_client import LLMModelClient
        from aphra.core.context import TranslationContext
        
        model_client = LLMModelClient(self.config_file)
        self.context = TranslationContext(
            model_client=model_client,
            source_language='English',
            target_language='Spanish',
            log_calls=False
        )

    def test_context_initialization(self):
        """
        Test initializing the TranslationContext.
        """
        self.assertIsNotNone(self.context.model_client)
        self.assertEqual(self.context.source_language, 'English')
        self.assertEqual(self.context.target_language, 'Spanish')
        self.assertFalse(self.context.log_calls)

if __name__ == '__main__':
    unittest.main()
