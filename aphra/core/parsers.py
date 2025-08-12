"""
Generic parsing utilities for XML-like content extraction.

This module provides generic parsers that can be used across different
workflows for extracting content from XML-like tags in LLM responses.
"""

import logging
import re
from typing import Optional

def parse_xml_tag(content: str, tag_name: str) -> Optional[str]:
    """
    Extract content from within XML-like tags in a string.

    This is a generic parser that can extract content from any XML-like tag
    in LLM responses, making it reusable across different workflows.

    Args:
        content: The string content containing XML-like tags
        tag_name: The name of the tag to extract (without < >)

    Returns:
        str: The content within the tags, or None if not found

    Example:
        >>> content = "Some text <result>Hello World</result> more text"
        >>> parse_xml_tag(content, "result")
        "Hello World"
    """
    try:
        start_tag = f"<{tag_name}>"
        end_tag = f"</{tag_name}>"

        start_index = content.find(start_tag)
        if start_index == -1:
            logging.warning("Start tag '<%s>' not found in content", tag_name)
            return None

        start_index += len(start_tag)
        end_index = content.find(end_tag, start_index)

        if end_index == -1:
            logging.warning("End tag '</%s>' not found in content", tag_name)
            return None

        extracted_content = content[start_index:end_index].strip()
        return extracted_content

    except Exception as exc:
        logging.error("Error parsing XML tag '%s': %s", tag_name, exc)
        return None

def parse_multiple_xml_tags(content: str, tag_name: str) -> list[str]:
    """
    Extract content from multiple XML-like tags of the same type.

    Args:
        content: The string content containing XML-like tags
        tag_name: The name of the tag to extract (without < >)

    Returns:
        list[str]: List of content within all matching tags

    Example:
        >>> content = "Text <item>First</item> more <item>Second</item> end"
        >>> parse_multiple_xml_tags(content, "item")
        ["First", "Second"]
    """
    try:
        # Use regex to find all occurrences
        pattern = f"<{re.escape(tag_name)}>(.*?)</{re.escape(tag_name)}>"
        matches = re.findall(pattern, content, re.DOTALL)

        # Strip whitespace from each match
        results = [match.strip() for match in matches]
        return results

    except Exception as exc:
        logging.error("Error parsing multiple XML tags '%s': %s", tag_name, exc)
        return []

def parse_xml_tag_with_attributes(content: str, tag_name: str) -> Optional[dict]:
    """
    Extract content and attributes from XML-like tags.

    Args:
        content: The string content containing XML-like tags
        tag_name: The name of the tag to extract (without < >)

    Returns:
        dict: Dictionary with 'content' and 'attributes' keys, or None if not found

    Example:
        >>> content = 'Text <result type="success">Hello World</result>'
        >>> parse_xml_tag_with_attributes(content, "result")
        {"content": "Hello World", "attributes": {"type": "success"}}
    """
    try:
        # Pattern to match tag with optional attributes
        pattern = f"<{re.escape(tag_name)}([^>]*)>(.*?)</{re.escape(tag_name)}>"
        match = re.search(pattern, content, re.DOTALL)

        if not match:
            logging.warning("Tag '<%s>' not found in content", tag_name)
            return None

        attributes_str = match.group(1).strip()
        tag_content = match.group(2).strip()

        # Parse attributes if any
        attributes = {}
        if attributes_str:
            # Simple attribute parsing (handles key="value" format)
            attr_pattern = r'(\w+)="([^"]*)"'
            attributes = dict(re.findall(attr_pattern, attributes_str))

        return {
            'content': tag_content,
            'attributes': attributes
        }

    except Exception as exc:
        logging.error("Error parsing XML tag with attributes '%s': %s", tag_name, exc)
        return None
