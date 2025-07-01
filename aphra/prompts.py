"""
Module for reading and formatting prompt templates.
"""

import os
from importlib import resources

def get_prompt(file_name, **kwargs):
    """
    Reads a prompt template from a file and formats it with the given arguments.

    :param file_name: Path to the file containing the prompt template.
    :param kwargs: Optional keyword arguments to format the prompt template.
    :return: The formatted prompt.
    """
    try:
        ref = resources.files(__package__) / 'prompts' / 'articles' / file_name
        with ref.open('r', encoding="utf-8") as file:
            content = file.read()
            if kwargs:
                formatted_prompt = content.format(**kwargs)
            else:
                formatted_prompt = content
        return formatted_prompt
    except (AttributeError, FileNotFoundError):
        file_path = os.path.join(os.path.dirname(__file__), 'prompts', 'articles', file_name)
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
            if kwargs:
                formatted_prompt = content.format(**kwargs)
            else:
                formatted_prompt = content
        return formatted_prompt
