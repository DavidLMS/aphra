"""
Test cases for the translate function in the aphra module.
"""

import unittest
from aphra.translate import translate, TranslationContext, load_model_client

class TestTranslate(unittest.TestCase):
    """
    Test cases for the translate function in the aphra module.
    """

    def setUp(self):
        """
        Set up the test case with default parameters.
        """
        self.source_language = 'Spanish'
        self.target_language = 'English'
        self.text = 'Hola mundo'
        self.config_file = 'config.toml'
        self.context = TranslationContext(load_model_client(self.config_file), 
                                          self.source_language, self.target_language, log_calls=False)

    def test_translation(self):
        """
        Test the translate function to ensure it returns a valid translation.
        """
        translation = translate(self.source_language, self.target_language, self.text, self.config_file, log_calls=False)
        self.assertIsNotNone(translation)

if __name__ == '__main__':
    unittest.main()
