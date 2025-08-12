"""
Workflow implementations with automatic discovery.

This module automatically discovers and imports all workflow classes
from subdirectories, making it easy to add new workflows without
modifying this file.
"""

import os
import importlib
import logging
from typing import List, Type, Dict

# Import the base class for type checking
try:
    from ..core.workflow import AbstractWorkflow
except ImportError:
    # Fallback for cases where core is not yet available
    AbstractWorkflow = None

logger = logging.getLogger(__name__)

# Initialize __all__ as empty list - will be populated by auto-discovery
__all__ = []

def _discover_workflows() -> Dict[str, Type]:
    """
    Auto-discover workflow classes from subdirectories.

    Scans all subdirectories of the workflows package and looks for
    classes that inherit from AbstractWorkflow.

    Returns:
        Dict[str, Type]: Mapping of class name to workflow class
    """
    workflows = {}
    current_dir = os.path.dirname(__file__)

    if not current_dir:
        logger.warning("Could not determine workflows directory")
        return workflows

    try:
        # Scan all items in the workflows directory
        for item in os.listdir(current_dir):
            item_path = os.path.join(current_dir, item)

            # Skip files and special directories
            if not os.path.isdir(item_path) or item.startswith('__'):
                continue

            # Skip if no __init__.py (not a proper Python package)
            init_file = os.path.join(item_path, '__init__.py')
            if not os.path.exists(init_file):
                logger.debug("Skipping %s: no __init__.py found", item)
                continue

            try:
                # Import the workflow package
                module = importlib.import_module(f'.{item}', package=__name__)
                logger.debug("Successfully imported workflow package: %s", item)

                # Look for workflow classes in the module
                workflow_classes_found = 0
                for attr_name in dir(module):
                    attr = getattr(module, attr_name, None)

                    # Check if it's a class that inherits from AbstractWorkflow
                    if (isinstance(attr, type) and
                        AbstractWorkflow is not None and
                        issubclass(attr, AbstractWorkflow) and
                        attr != AbstractWorkflow):

                        workflows[attr_name] = attr
                        workflow_classes_found += 1
                        logger.debug("Discovered workflow: %s from %s", attr_name, item)

                if workflow_classes_found == 0:
                    logger.warning("No workflow classes found in %s", item)

            except ImportError as exc:
                logger.warning("Failed to import workflow package %s: %s", item, exc)
                continue
            except Exception as exc:
                logger.error("Unexpected error while discovering workflow %s: %s", item, exc)
                continue

    except OSError as exc:
        logger.error("Failed to scan workflows directory: %s", exc)

    logger.debug("Workflow discovery completed. Found %d workflows: %s",
                 len(workflows), list(workflows.keys()))
    return workflows

def _setup_module_exports(workflows: Dict[str, Type]) -> List[str]:
    """
    Set up module-level exports for discovered workflows.

    Args:
        workflows: Dictionary of workflow name to class mappings
    
    Returns:
        List[str]: List of exported workflow class names
    """
    exported_classes = []

    # Add each workflow class to the module globals and collect names
    for class_name, workflow_class in workflows.items():
        globals()[class_name] = workflow_class
        exported_classes.append(class_name)

    # Sort for consistency
    exported_classes.sort()
    return exported_classes

# Perform auto-discovery
logger.debug("Starting workflow auto-discovery...")
_discovered_workflows = _discover_workflows()

# Set up module exports
__all__ = _setup_module_exports(_discovered_workflows)

# Log final state
logger.debug("Workflows module initialized with: %s", __all__)

# For backward compatibility and explicit access
def get_available_workflows() -> List[str]:
    """
    Get a list of all available workflow class names.

    Returns:
        List[str]: List of available workflow class names
    """
    return list(__all__)

def get_workflow_class(name: str) -> Type:
    """
    Get a workflow class by name.

    Args:
        name: The name of the workflow class

    Returns:
        Type: The workflow class

    Raises:
        AttributeError: If the workflow class is not found
    """
    if name not in globals():
        raise AttributeError(f"Workflow class '{name}' not found. Available: {__all__}")

    return globals()[name]
