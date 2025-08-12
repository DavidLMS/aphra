"""
Parsers specific to the Short Article workflow.

This module contains parsers for extracting content from LLM responses
that are specific to the short article translation workflow.

These parsers use the generic XML parsing functions from the core module
to avoid code duplication while maintaining a clear API.
"""

import logging
from typing import List, Dict, Any
from ....core.parsers import parse_xml_tag, parse_multiple_xml_tags

def parse_analysis(analysis_str: str) -> List[Dict[str, Any]]:
    """
    Parses the analysis part of the provided string and returns
    a list of items with their names and keywords.

    Uses generic XML parsers from the core module to extract structured data
    from the <analysis> tag and its nested <item> elements.

    Args:
        analysis_str: String containing the analysis in the specified format.

    Returns:
        List[Dict]: A list of dictionaries, each containing 'name' and 'keywords' from the analysis.
    """
    # 1. Extract content of <analysis> tag
    analysis_content = parse_xml_tag(analysis_str, "analysis")
    if not analysis_content:
        logging.error('Could not find <analysis> tag in content')
        return []

    # 2. Extract all <item> tags within the analysis
    item_contents = parse_multiple_xml_tags(analysis_content, "item")
    if not item_contents:
        logging.warning('No <item> tags found within <analysis>')
        return []

    # 3. For each item, extract name and keywords
    items = []
    for item_content in item_contents:
        name = parse_xml_tag(item_content, "name")
        keywords_str = parse_xml_tag(item_content, "keywords")

        if name and keywords_str:
            items.append({
                'name': name,
                'keywords': keywords_str.split(', ')
            })
        else:
            logging.warning('Incomplete item found - name: %s, keywords: %s', name, keywords_str)

    return items

def parse_translation(translation_str: str) -> str:
    """
    Parses the provided string and returns the content within
    <improved_translation> tags.

    Uses the generic XML parser from the core module to extract the translation.

    Args:
        translation_str: String containing the translation in the specified format.

    Returns:
        str: String containing the <improved_translation> content.
    """
    result = parse_xml_tag(translation_str, "improved_translation")
    if result is None:
        logging.error('Could not find <improved_translation> tag in content')
        return ""

    return result
