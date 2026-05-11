import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "click here", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">click here</a>'
        )

    def test_leaf_to_html_a_multiple_props(self):
        node = LeafNode(
            "a", "click here", {"href": "https://www.google.com", "foo": "barbaz"}
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com" foo="barbaz">click here</a>',
        )
