"""
Test cases for the translate function in the aphra module.
"""

import importlib
import unittest
from unittest.mock import patch, MagicMock

# Use importlib to get the actual module, not the function exposed by aphra.__init__
translate_module = importlib.import_module('aphra.translate')
translate = translate_module.translate


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

    def test_translation(self):
        """
        Test the translate function to ensure it returns a valid translation.
        """
        translation = translate(
            self.source_language,
            self.target_language,
            self.text,
            self.config_file,
            log_calls=False
        )
        self.assertIsNotNone(translation)


class TestTranslateWorkflowSelection(unittest.TestCase):
    """
    Test cases for the workflow selection logic in translate().
    """

    @patch.object(translate_module, 'load_model_client')
    @patch.object(translate_module, 'get_workflow')
    def test_explicit_workflow_is_used(self, mock_get_workflow, mock_load_client):
        """
        Test that passing workflow='short_article' uses that workflow.
        """
        mock_wf = MagicMock()
        mock_wf.run.return_value = 'translated text'
        mock_get_workflow.return_value = mock_wf

        result = translate('Spanish', 'English', 'Hola', workflow='short_article')

        mock_get_workflow.assert_called_once_with('short_article')
        mock_wf.run.assert_called_once()
        self.assertEqual(result, 'translated text')

    @patch.object(translate_module, 'load_model_client')
    @patch.object(translate_module, 'get_registry')
    @patch.object(translate_module, 'get_workflow')
    def test_unknown_workflow_raises_with_available(self, mock_get_workflow, mock_get_registry, mock_load_client):
        """
        Test that an unknown workflow raises ValueError listing available workflows.
        """
        mock_get_workflow.return_value = None
        mock_registry = MagicMock()
        mock_registry.list_workflows.return_value = ['short_article', 'subtitle']
        mock_get_registry.return_value = mock_registry

        with self.assertRaises(ValueError) as ctx:
            translate('Spanish', 'English', 'Hola', workflow='nonexistent')

        self.assertIn('nonexistent', str(ctx.exception))
        self.assertIn('short_article', str(ctx.exception))
        self.assertIn('subtitle', str(ctx.exception))

    @patch.object(translate_module, 'load_model_client')
    @patch.object(translate_module, 'get_suitable_workflow')
    def test_auto_selection_when_no_workflow_specified(self, mock_get_suitable, mock_load_client):
        """
        Test that workflow=None triggers auto-selection.
        """
        mock_wf = MagicMock()
        mock_wf.run.return_value = 'auto translated'
        mock_get_suitable.return_value = mock_wf

        result = translate('Spanish', 'English', 'Hola')

        mock_get_suitable.assert_called_once_with('Hola')
        self.assertEqual(result, 'auto translated')

    @patch.object(translate_module, 'load_model_client')
    @patch.object(translate_module, 'get_suitable_workflow')
    def test_auto_selection_no_suitable_raises(self, mock_get_suitable, mock_load_client):
        """
        Test that auto-selection raises ValueError when no workflow matches.
        """
        mock_get_suitable.return_value = None

        with self.assertRaises(ValueError) as ctx:
            translate('Spanish', 'English', '')

        self.assertIn('No suitable workflow', str(ctx.exception))


if __name__ == '__main__':
    unittest.main()
