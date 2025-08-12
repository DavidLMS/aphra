"""
Test cases for the generic XML parser functions in the core module.

These tests verify the generic parsing functionality that can be used
across all workflows.
"""

import unittest
from aphra.core.parsers import (
    parse_xml_tag, 
    parse_multiple_xml_tags, 
    parse_xml_tag_with_attributes
)


class TestCoreParsers(unittest.TestCase):
    """
    Test cases for the core generic XML parser functions.
    """

    def test_parse_xml_tag_simple(self):
        """
        Test parsing a simple XML tag.
        """
        content = "Some text <result>Hello World</result> more text"
        result = parse_xml_tag(content, "result")
        self.assertEqual(result, "Hello World")

    def test_parse_xml_tag_multiline(self):
        """
        Test parsing XML tag with multiline content.
        """
        content = """Some text
        <result>
        Hello
        World
        </result>
        more text"""
        result = parse_xml_tag(content, "result")
        self.assertEqual(result.strip(), "Hello\n        World")

    def test_parse_xml_tag_missing(self):
        """
        Test parsing when tag is missing.
        """
        content = "Some text without the tag"
        result = parse_xml_tag(content, "result")
        self.assertIsNone(result)

    def test_parse_xml_tag_empty(self):
        """
        Test parsing empty XML tag.
        """
        content = "Some text <result></result> more text"
        result = parse_xml_tag(content, "result")
        self.assertEqual(result, "")

    def test_parse_multiple_xml_tags(self):
        """
        Test parsing multiple XML tags of the same type.
        """
        content = "Text <item>First</item> more <item>Second</item> end"
        results = parse_multiple_xml_tags(content, "item")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], "First")
        self.assertEqual(results[1], "Second")

    def test_parse_multiple_xml_tags_empty(self):
        """
        Test parsing when no matching tags exist.
        """
        content = "Text without any matching tags"
        results = parse_multiple_xml_tags(content, "item")
        self.assertEqual(len(results), 0)

    def test_parse_multiple_xml_tags_nested_content(self):
        """
        Test parsing multiple XML tags with nested content.
        """
        content = """
        <item>
            <name>First</name>
            <value>A</value>
        </item>
        <item>
            <name>Second</name>
            <value>B</value>
        </item>
        """
        results = parse_multiple_xml_tags(content, "item")
        self.assertEqual(len(results), 2)
        self.assertIn("<name>First</name>", results[0])
        self.assertIn("<name>Second</name>", results[1])

    def test_parse_xml_tag_with_attributes_simple(self):
        """
        Test parsing XML tag with simple attributes.
        """
        content = 'Text <result type="success">Hello World</result>'
        result = parse_xml_tag_with_attributes(content, "result")
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['content'], "Hello World")
        self.assertEqual(result['attributes']['type'], "success")

    def test_parse_xml_tag_with_attributes_multiple(self):
        """
        Test parsing XML tag with multiple attributes.
        """
        content = 'Text <result type="success" code="200">Hello World</result>'
        result = parse_xml_tag_with_attributes(content, "result")
        
        self.assertEqual(result['content'], "Hello World")
        self.assertEqual(result['attributes']['type'], "success")
        self.assertEqual(result['attributes']['code'], "200")

    def test_parse_xml_tag_with_attributes_no_attributes(self):
        """
        Test parsing XML tag without attributes.
        """
        content = 'Text <result>Hello World</result>'
        result = parse_xml_tag_with_attributes(content, "result")
        
        self.assertEqual(result['content'], "Hello World")
        self.assertEqual(len(result['attributes']), 0)

    def test_parse_xml_tag_with_attributes_missing(self):
        """
        Test parsing when tag with attributes is missing.
        """
        content = "Text without the tag"
        result = parse_xml_tag_with_attributes(content, "result")
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()