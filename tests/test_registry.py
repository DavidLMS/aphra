"""
Test cases for the workflow registry and auto-discovery system.

These tests verify that the registry correctly discovers and manages workflows.
"""

import unittest
from aphra.core.registry import WorkflowRegistry, get_registry, get_workflow
from aphra.core.workflow import AbstractWorkflow


class TestWorkflowRegistry(unittest.TestCase):
    """
    Test cases for the workflow registry system.
    """

    def setUp(self):
        """Set up test cases with a fresh registry instance."""
        self.registry = WorkflowRegistry()

    def test_registry_initialization(self):
        """
        Test that registry initializes and discovers workflows.
        """
        # Should discover at least the short_article workflow
        workflows = self.registry.list_workflows()
        self.assertGreater(len(workflows), 0)
        self.assertIn('short_article', workflows)

    def test_get_workflow_by_name(self):
        """
        Test retrieving a workflow by name.
        """
        workflow = self.registry.get_workflow('short_article')
        self.assertIsNotNone(workflow)
        self.assertIsInstance(workflow, AbstractWorkflow)
        self.assertEqual(workflow.get_workflow_name(), 'short_article')

    def test_get_workflow_missing(self):
        """
        Test retrieving a non-existent workflow.
        """
        workflow = self.registry.get_workflow('nonexistent_workflow')
        self.assertIsNone(workflow)

    def test_suitable_workflow_discovery(self):
        """
        Test finding suitable workflow for content.
        """
        # Should find short_article workflow for general text
        workflow = self.registry.get_suitable_workflow('Hello world')
        self.assertIsNotNone(workflow)
        self.assertEqual(workflow.get_workflow_name(), 'short_article')

    def test_suitable_workflow_none_found(self):
        """
        Test when no suitable workflow is found.
        """
        # Empty text should not match any workflow
        workflow = self.registry.get_suitable_workflow('')
        self.assertIsNone(workflow)

    def test_workflow_info(self):
        """
        Test getting information about a workflow.
        """
        info = self.registry.get_workflow_info('short_article')
        self.assertIsNotNone(info)
        self.assertIn('name', info)
        self.assertIn('class', info)
        self.assertIn('module', info)
        self.assertEqual(info['name'], 'short_article')

    def test_workflow_info_missing(self):
        """
        Test getting info for non-existent workflow.
        """
        info = self.registry.get_workflow_info('nonexistent_workflow')
        self.assertIsNone(info)

    def test_global_registry_singleton(self):
        """
        Test that get_registry returns the same instance.
        """
        registry1 = get_registry()
        registry2 = get_registry()
        self.assertIs(registry1, registry2)

    def test_global_get_workflow_function(self):
        """
        Test the global get_workflow convenience function.
        """
        workflow = get_workflow('short_article')
        self.assertIsNotNone(workflow)
        self.assertEqual(workflow.get_workflow_name(), 'short_article')


class TestWorkflowAutoDiscovery(unittest.TestCase):
    """
    Test cases for the auto-discovery system.
    """

    def test_workflows_module_discovery(self):
        """
        Test that workflows are auto-discovered in the workflows module.
        """
        from aphra.workflows import __all__, get_available_workflows
        
        # Should discover at least ShortArticleWorkflow
        self.assertGreater(len(__all__), 0)
        self.assertIn('ShortArticleWorkflow', __all__)
        
        # get_available_workflows should return the same list
        available = get_available_workflows()
        self.assertEqual(available, __all__)

    def test_workflow_class_access(self):
        """
        Test that discovered workflow classes are accessible.
        """
        from aphra.workflows import ShortArticleWorkflow, get_workflow_class
        
        # Direct import should work
        self.assertIsNotNone(ShortArticleWorkflow)
        self.assertTrue(issubclass(ShortArticleWorkflow, AbstractWorkflow))
        
        # get_workflow_class function should work
        workflow_class = get_workflow_class('ShortArticleWorkflow')
        self.assertIs(workflow_class, ShortArticleWorkflow)

    def test_workflow_class_access_missing(self):
        """
        Test accessing non-existent workflow class.
        """
        from aphra.workflows import get_workflow_class
        
        with self.assertRaises(AttributeError):
            get_workflow_class('NonexistentWorkflow')

    def test_discovery_integration_with_registry(self):
        """
        Test that auto-discovery integrates correctly with registry.
        """
        from aphra.workflows import __all__
        
        registry = get_registry()
        registry_workflows = registry.list_workflows()
        
        # Every discovered workflow should be registered
        # (Though names might be different - class name vs workflow name)
        self.assertGreater(len(registry_workflows), 0)
        
        # At least short_article should be present
        self.assertIn('short_article', registry_workflows)


if __name__ == '__main__':
    unittest.main()