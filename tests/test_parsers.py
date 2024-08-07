"""
Test cases for the parser functions in the aphra module.
"""

import unittest
from aphra.parsers import parse_analysis, parse_translation

class TestParsers(unittest.TestCase):
    """
    Test cases for the parser functions in the aphra module.
    """

    def test_parse_analysis(self):
        """
        Test parsing an analysis string into items.
        """
        analysis_str = (
            "<analysis><item><name>Hola</name><keywords>hello, hi</keywords></item></analysis>"
        )
        parsed = parse_analysis(analysis_str)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]['name'], 'Hola')
        self.assertIn('hello', parsed[0]['keywords'])

    def test_parse_translation(self):
        """
        Test parsing a translation string into improved translation content.
        """
        translation_str = "<improved_translation>Hello world</improved_translation>"
        translation = parse_translation(translation_str)
        self.assertEqual(translation, 'Hello world')

if __name__ == '__main__':
    unittest.main()
