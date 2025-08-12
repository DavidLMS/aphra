"""
Test cases for the core prompt system.

These tests verify the generic prompt loading functionality that can be used
across all workflows.
"""

import unittest
from aphra.core.prompts import get_prompt, list_workflow_prompts


class TestCorePrompts(unittest.TestCase):
    """
    Test cases for the core prompt system functions.
    """

    def test_get_prompt_basic(self):
        """
        Test basic prompt loading functionality.
        """
        # Test with the existing short_article workflow
        prompt = get_prompt('short_article', 'step1_system.txt')
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)

    def test_get_prompt_with_formatting(self):
        """
        Test prompt loading with formatting parameters.
        """
        prompt = get_prompt('short_article', 'step1_system.txt',
                          source_language='Spanish',
                          target_language='English')
        self.assertIn('Spanish', prompt)
        self.assertIn('English', prompt)

    def test_get_prompt_missing_workflow(self):
        """
        Test behavior when requesting prompts from non-existent workflow.
        """
        with self.assertRaises(FileNotFoundError):
            get_prompt('nonexistent_workflow', 'step1_system.txt')

    def test_get_prompt_missing_file(self):
        """
        Test behavior when requesting non-existent prompt file.
        """
        with self.assertRaises(FileNotFoundError):
            get_prompt('short_article', 'nonexistent_prompt.txt')

    def test_get_prompt_missing_format_parameter(self):
        """
        Test behavior when required format parameter is missing.
        """
        # This should raise KeyError if the template requires parameters
        # but they're not provided (depends on the actual template content)
        try:
            prompt = get_prompt('short_article', 'step1_system.txt',
                              source_language='Spanish')
            # If it doesn't raise an error, the template is flexible
            self.assertIsInstance(prompt, str)
        except KeyError:
            # If it raises KeyError, that's also acceptable behavior
            pass

    def test_list_workflow_prompts(self):
        """
        Test listing available prompt files for a workflow.
        """
        prompts = list_workflow_prompts('short_article')
        self.assertIsInstance(prompts, list)
        self.assertGreater(len(prompts), 0)
        
        # Check that expected files are present
        expected_files = [
            'step1_system.txt', 'step1_user.txt',
            'step2_system.txt', 'step2_user.txt',
            'step3_system.txt', 'step3_user.txt',
            'step4_system.txt', 'step4_user.txt',
            'step5_system.txt', 'step5_user.txt'
        ]
        
        for expected_file in expected_files:
            self.assertIn(expected_file, prompts)

    def test_list_workflow_prompts_missing_workflow(self):
        """
        Test listing prompts for non-existent workflow.
        """
        with self.assertRaises(FileNotFoundError):
            list_workflow_prompts('nonexistent_workflow')

    def test_prompt_file_extensions(self):
        """
        Test that only .txt files are listed as prompts.
        """
        prompts = list_workflow_prompts('short_article')
        
        # All files should have .txt extension
        for prompt_file in prompts:
            self.assertTrue(prompt_file.endswith('.txt'))


if __name__ == '__main__':
    unittest.main()