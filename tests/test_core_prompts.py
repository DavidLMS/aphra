"""
Test cases for the core prompt system.

These tests verify the generic prompt loading functionality that can be used
across all workflows, including the prompt override system (prompts_dir).
"""

import os
import shutil
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from aphra.core.prompts import get_prompt, list_workflow_prompts
from aphra.core.context import TranslationContext
from aphra.core.workflow import AbstractWorkflow


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


class TestPromptOverrides(unittest.TestCase):
    """
    Test cases for the prompt override system (prompts_dir).
    """

    def setUp(self):
        """Create a temporary directory for prompt overrides."""
        self._tmpdir = tempfile.TemporaryDirectory()
        self.tmpdir = self._tmpdir.name

    def tearDown(self):
        """Clean up temporary directory."""
        self._tmpdir.cleanup()

    def test_full_override(self):
        """
        Test that a file in prompts_dir completely replaces the default prompt.
        """
        override_content = "Custom prompt for {source_language} to {target_language}."
        override_path = os.path.join(self.tmpdir, 'step1_system.txt')
        with open(override_path, 'w', encoding='utf-8') as f:
            f.write(override_content)

        result = get_prompt('short_article', 'step1_system.txt',
                           prompts_dir=self.tmpdir,
                           source_language='Spanish',
                           target_language='English')

        self.assertEqual(result, "Custom prompt for Spanish to English.")

    def test_append(self):
        """
        Test that an _append file adds content after the default prompt.
        """
        append_content = "APPENDED INSTRUCTION"
        append_path = os.path.join(self.tmpdir, 'step1_system_append.txt')
        with open(append_path, 'w', encoding='utf-8') as f:
            f.write(append_content)

        result = get_prompt('short_article', 'step1_system.txt',
                           prompts_dir=self.tmpdir)

        # Default prompt should be there, followed by the appended content
        self.assertTrue(result.endswith("APPENDED INSTRUCTION"))
        self.assertGreater(len(result), len(append_content))

    def test_prepend(self):
        """
        Test that a _prepend file adds content before the default prompt.
        """
        prepend_content = "PREPENDED INSTRUCTION"
        prepend_path = os.path.join(self.tmpdir, 'step1_system_prepend.txt')
        with open(prepend_path, 'w', encoding='utf-8') as f:
            f.write(prepend_content)

        result = get_prompt('short_article', 'step1_system.txt',
                           prompts_dir=self.tmpdir)

        # Prepended content should be at the start
        self.assertTrue(result.startswith("PREPENDED INSTRUCTION"))
        self.assertGreater(len(result), len(prepend_content))

    def test_prepend_and_append_together(self):
        """
        Test that prepend and append can be used simultaneously.
        """
        prepend_path = os.path.join(self.tmpdir, 'step1_system_prepend.txt')
        with open(prepend_path, 'w', encoding='utf-8') as f:
            f.write("BEFORE")

        append_path = os.path.join(self.tmpdir, 'step1_system_append.txt')
        with open(append_path, 'w', encoding='utf-8') as f:
            f.write("AFTER")

        result = get_prompt('short_article', 'step1_system.txt',
                           prompts_dir=self.tmpdir)

        self.assertTrue(result.startswith("BEFORE"))
        self.assertTrue(result.endswith("AFTER"))

    def test_override_takes_priority_over_append_and_prepend(self):
        """
        Test that a full override ignores both append and prepend files.
        """
        override_path = os.path.join(self.tmpdir, 'step1_system.txt')
        with open(override_path, 'w', encoding='utf-8') as f:
            f.write("OVERRIDE ONLY")

        append_path = os.path.join(self.tmpdir, 'step1_system_append.txt')
        with open(append_path, 'w', encoding='utf-8') as f:
            f.write("SHOULD NOT APPEAR")

        prepend_path = os.path.join(self.tmpdir, 'step1_system_prepend.txt')
        with open(prepend_path, 'w', encoding='utf-8') as f:
            f.write("SHOULD NOT APPEAR EITHER")

        result = get_prompt('short_article', 'step1_system.txt',
                           prompts_dir=self.tmpdir)

        self.assertEqual(result, "OVERRIDE ONLY")
        self.assertNotIn("SHOULD NOT APPEAR", result)

    def test_no_prompts_dir_uses_default(self):
        """
        Test that omitting prompts_dir loads the default prompt (backwards compatible).
        """
        result_without = get_prompt('short_article', 'step1_system.txt')
        result_with_none = get_prompt('short_article', 'step1_system.txt', prompts_dir=None)

        self.assertEqual(result_without, result_with_none)
        self.assertGreater(len(result_without), 0)

    def test_empty_prompts_dir_uses_default(self):
        """
        Test that an empty prompts_dir falls through to the default prompt.
        """
        result_default = get_prompt('short_article', 'step1_system.txt')
        result_empty_dir = get_prompt('short_article', 'step1_system.txt',
                                      prompts_dir=self.tmpdir)

        self.assertEqual(result_default, result_empty_dir)

    def test_append_with_placeholders(self):
        """
        Test that append files support the same {placeholders}.
        """
        append_content = "Extra instructions for {source_language} to {target_language}."
        append_path = os.path.join(self.tmpdir, 'step1_system_append.txt')
        with open(append_path, 'w', encoding='utf-8') as f:
            f.write(append_content)

        result = get_prompt('short_article', 'step1_system.txt',
                           prompts_dir=self.tmpdir,
                           source_language='Spanish',
                           target_language='English')

        self.assertTrue(result.endswith("Extra instructions for Spanish to English."))


class TestWorkflowPromptOverrideIntegration(unittest.TestCase):
    """
    Integration test: AbstractWorkflow.run() wires prompts_dir into self.get_prompt().
    """

    def setUp(self):
        """Create a temporary directory and a concrete workflow for testing."""
        self._tmpdir = tempfile.TemporaryDirectory()
        self.tmpdir = self._tmpdir.name

        # Create a minimal concrete workflow for testing
        class DummyWorkflow(AbstractWorkflow):
            def __init__(self):
                super().__init__()
                self.last_prompt = None

            def get_workflow_name(self):
                return "short_article"

            def is_suitable_for(self, text, **kwargs):
                return True

            def execute(self, context, text):
                # Use self.get_prompt() which should pick up prompts_dir
                self.last_prompt = self.get_prompt('step1_system.txt')
                return "done"

        self.DummyWorkflow = DummyWorkflow

    def tearDown(self):
        """Clean up temporary directory."""
        self._tmpdir.cleanup()

    @patch('aphra.core.workflow.load_workflow_config')
    def test_run_wires_prompts_dir_into_get_prompt(self, mock_load_config):
        """
        Test that run() reads prompts_dir from config and self.get_prompt() uses it.
        """
        # Create an override file
        override_path = os.path.join(self.tmpdir, 'step1_system.txt')
        with open(override_path, 'w', encoding='utf-8') as f:
            f.write("OVERRIDDEN VIA WORKFLOW")

        # Mock config to return our prompts_dir
        mock_load_config.return_value = {
            'writer': 'test-model',
            'prompts_dir': self.tmpdir
        }

        workflow = self.DummyWorkflow()
        context = MagicMock(spec=TranslationContext)

        workflow.run(context, "test text")

        self.assertEqual(workflow.last_prompt, "OVERRIDDEN VIA WORKFLOW")

    @patch('aphra.core.workflow.load_workflow_config')
    def test_run_without_prompts_dir_uses_defaults(self, mock_load_config):
        """
        Test that run() without prompts_dir in config uses default prompts.
        """
        mock_load_config.return_value = {'writer': 'test-model'}

        workflow = self.DummyWorkflow()
        context = MagicMock(spec=TranslationContext)

        workflow.run(context, "test text")

        # Should load the default prompt (non-empty)
        self.assertIsNotNone(workflow.last_prompt)
        self.assertGreater(len(workflow.last_prompt), 0)
        self.assertNotEqual(workflow.last_prompt, "OVERRIDDEN VIA WORKFLOW")


if __name__ == '__main__':
    unittest.main()
