import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_attrs_default_to_none(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_props_to_html_with_props(self):
        node = HTMLNode(
            "<p>",
            "foobar",
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        assert node.props_to_html() == ' href="https://www.google.com" target="_blank"'

    def test_props_to_html_without_props(self):
        node = HTMLNode("<p>", "foobar", None, None)
        assert node.props_to_html() == ""

    def test_to_html_raises_error(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()
