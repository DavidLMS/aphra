"""
Test cases for the TranslationContext class in the aphra module.
"""

import unittest
from test_utils import create_translation_context

class TestTranslationContext(unittest.TestCase):
    """
    Test cases for the TranslationContext class in the aphra module.
    """

    def setUp(self):
        """
        Set up the test case with default parameters.
        """
        self.config_file = 'config.toml'
        self.context = create_translation_context(self.config_file, 
                                                  'Spanish', 
                                                  'English', 
                                                  log_calls=False)

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
