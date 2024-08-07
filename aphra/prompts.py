"""
Module for reading and formatting prompt templates.
"""

from pkg_resources import resource_filename

def get_prompt(file_name, **kwargs):
    """
    Reads a prompt template from a file and formats it with the given arguments.

    :param file_name: Path to the file containing the prompt template.
    :param kwargs: Optional keyword arguments to format the prompt template.
    :return: The formatted prompt.
    """
    file_path = resource_filename(__name__, f'prompts/{file_name}')
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        if kwargs:
            formatted_prompt = content.format(**kwargs)
        else:
            formatted_prompt = content
    return formatted_prompt
