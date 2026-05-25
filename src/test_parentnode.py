import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_no_tag(self):
        parent_node = ParentNode(None, None)
        with self.assertRaises(ValueError) as e:
            parent_node.to_html()
        self.assertEqual(str(e.exception), "all parent nodes must have a tag")

    def test_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as e:
            parent_node.to_html()
        self.assertEqual(
            str(e.exception), "all parent nodes must have at least one child"
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_children_with_props(self):
        child_node = LeafNode("a", "click here", {"href": "https://www.google.com"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><a href="https://www.google.com">click here</a></div>',
        )

    def test_to_html_many_children(self):
        parent_node = ParentNode(
            "p",
            [
                LeafNode("b", "bold"),
                LeafNode(None, " plain "),
                LeafNode("i", "italic"),
            ],
        )
        self.assertEqual(
            parent_node.to_html(), "<p><b>bold</b> plain <i>italic</i></p>"
        )

    def test_to_html_deeply_nested(self):
        node = ParentNode(
            "div", [ParentNode("section", [ParentNode("p", [LeafNode("b", "deep")])])]
        )
        self.assertEqual(
            node.to_html(), "<div><section><p><b>deep</b></p></section></div>"
        )

    def test_to_html_with_props_in_parent(self):
        node = ParentNode(
            "a", [LeafNode(None, "click me")], {"href": "https://example.com"}
        )
        self.assertEqual(node.to_html(), '<a href="https://example.com">click me</a>')
