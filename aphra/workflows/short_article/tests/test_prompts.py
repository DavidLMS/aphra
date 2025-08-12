"""
Test cases for prompt functionality specific to the Short Article workflow.

These tests verify that the workflow can correctly load and format
its specific prompt templates.
"""

import unittest
from ....core.prompts import get_prompt

class TestShortArticlePrompts(unittest.TestCase):
    """
    Test cases for the short article workflow prompt functions.
    """

    def test_get_prompt_with_formatting(self):
        """
        Test getting a prompt and formatting it correctly with the new signature.
        """
        file_name = 'step1_system.txt'
        prompt = get_prompt('short_article', file_name,
                          source_language='Spanish',
                          target_language='English')

        # Verify that the prompt contains the formatted languages
        self.assertIn('Spanish', prompt)
        self.assertIn('English', prompt)

    def test_get_prompt_without_formatting(self):
        """
        Test getting a prompt without formatting parameters.
        """
        file_name = 'step1_system.txt'
        prompt = get_prompt('short_article', file_name)

        # Should return the prompt template content
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)

    def test_get_prompt_all_steps(self):
        """
        Test that all prompt files for the workflow can be loaded.
        """
        step_files = [
            'step1_system.txt', 'step1_user.txt',
            'step2_system.txt', 'step2_user.txt',
            'step3_system.txt', 'step3_user.txt',
            'step4_system.txt', 'step4_user.txt',
            'step5_system.txt', 'step5_user.txt'
        ]

        for file_name in step_files:
            with self.subTest(file_name=file_name):
                prompt = get_prompt('short_article', file_name)
                self.assertIsInstance(prompt, str)
                self.assertGreater(len(prompt), 0)

    def test_get_prompt_missing_file(self):
        """
        Test behavior when requesting a non-existent prompt file.
        """
        with self.assertRaises(FileNotFoundError):
            get_prompt('short_article', 'nonexistent_prompt.txt')

    def test_get_prompt_missing_workflow(self):
        """
        Test behavior when requesting prompts from a non-existent workflow.
        """
        with self.assertRaises(FileNotFoundError):
            get_prompt('nonexistent_workflow', 'step1_system.txt')

if __name__ == '__main__':
    unittest.main()
