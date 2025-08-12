"""
Test cases for the parser functions specific to the Short Article workflow.

These tests verify that the workflow-specific parsers work correctly
using the generic core parsers internally.
"""

import unittest
from ..aux.parsers import parse_analysis, parse_translation

class TestShortArticleParsers(unittest.TestCase):
    """
    Test cases for the short article workflow-specific parser functions.
    """

    def test_parse_analysis(self):
        """
        Test parsing an analysis string into items using the new generic parsers.
        """
        analysis_str = (
            "<analysis><item><name>Hola</name><keywords>hello, hi</keywords></item></analysis>"
        )
        parsed = parse_analysis(analysis_str)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]['name'], 'Hola')
        self.assertIn('hello', parsed[0]['keywords'])

    def test_parse_analysis_multiple_items(self):
        """
        Test parsing an analysis string with multiple items.
        """
        analysis_str = (
            "<analysis>"
            "<item><name>Hola</name><keywords>hello, hi</keywords></item>"
            "<item><name>Mundo</name><keywords>world, earth</keywords></item>"
            "</analysis>"
        )
        parsed = parse_analysis(analysis_str)
        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0]['name'], 'Hola')
        self.assertEqual(parsed[1]['name'], 'Mundo')
        self.assertIn('hello', parsed[0]['keywords'])
        self.assertIn('world', parsed[1]['keywords'])

    def test_parse_analysis_empty(self):
        """
        Test parsing an empty or invalid analysis string.
        """
        # Empty analysis
        parsed = parse_analysis("<analysis></analysis>")
        self.assertEqual(len(parsed), 0)

        # No analysis tag
        parsed = parse_analysis("No analysis here")
        self.assertEqual(len(parsed), 0)

    def test_parse_translation(self):
        """
        Test parsing a translation string into improved translation content.
        """
        translation_str = "<improved_translation>Hello world</improved_translation>"
        translation = parse_translation(translation_str)
        self.assertEqual(translation, "Hello world")

    def test_parse_translation_with_extra_content(self):
        """
        Test parsing translation with content before and after the tag.
        """
        translation_str = (
            "Some preamble text\n"
            "<improved_translation>Hello beautiful world</improved_translation>\n"
            "Some postamble text"
        )
        translation = parse_translation(translation_str)
        self.assertEqual(translation, "Hello beautiful world")

    def test_parse_translation_missing_tag(self):
        """
        Test parsing translation when the tag is missing.
        """
        translation_str = "Just some text without tags"
        translation = parse_translation(translation_str)
        self.assertEqual(translation, "")

    def test_parse_translation_empty_tag(self):
        """
        Test parsing translation with empty tag.
        """
        translation_str = "<improved_translation></improved_translation>"
        translation = parse_translation(translation_str)
        self.assertEqual(translation, "")

if __name__ == '__main__':
    unittest.main()
