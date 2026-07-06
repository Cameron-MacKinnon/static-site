import unittest

from src.split_delimiter import split_nodes_delimiter
from src.textnode import TextNode, TextType


class TestSplitDelimiter(unittest.TestCase):
    def test_basic_code(self):
        node = TextNode("This `contains` a code block", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This ", TextType.PLAIN, None),
            TextNode("contains", TextType.CODE, None),
            TextNode(" a code block", TextType.PLAIN, None),
        ]
        self.assertEqual(new_nodes, expected)

    def test_basic_italic(self):
        node = TextNode("This contains _italic_ text", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This contains ", TextType.PLAIN, None),
            TextNode("italic", TextType.ITALIC, None),
            TextNode(" text", TextType.PLAIN, None),
        ]
        self.assertEqual(new_nodes, expected)

    def test_basic_bold(self):
        node = TextNode("This contains **bold** text", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This contains ", TextType.PLAIN, None),
            TextNode("bold", TextType.BOLD, None),
            TextNode(" text", TextType.PLAIN, None),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delimiter_at_start(self):
        node = TextNode("**This** contains bold text", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This", TextType.BOLD, None),
            TextNode(" contains bold text", TextType.PLAIN, None),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delimiter_at_end(self):
        node = TextNode("This contains bold **text**", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This contains bold ", TextType.PLAIN, None),
            TextNode("text", TextType.BOLD, None),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_instances_of_delimiter(self):
        node = TextNode("This is just text", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [TextNode("This is just text", TextType.PLAIN)]
        self.assertEqual(new_nodes, expected)

    def test_multiple_instances_of_delimiter(self):
        node = TextNode(
            "This contains **bold text**, and then **even more** bold text",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This contains ", TextType.PLAIN, None),
            TextNode("bold text", TextType.BOLD, None),
            TextNode(", and then ", TextType.PLAIN, None),
            TextNode("even more", TextType.BOLD, None),
            TextNode(" bold text", TextType.PLAIN, None),
        ]
        self.assertEqual(new_nodes, expected)

    def test_invalid_delimiter(self):
        node = TextNode("This is just text", TextType.PLAIN)
        with self.assertRaises(ValueError):
            new_nodes = split_nodes_delimiter([node], "%", TextType.ITALIC)

    def test_multiple_nodes(self):
        node_1 = TextNode("This contains **bold** text", TextType.PLAIN)
        node_2 = TextNode("This also contains **bold** text", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node_1, node_2], "**", TextType.BOLD)
        expected = [
            TextNode("This contains ", TextType.PLAIN, None),
            TextNode("bold", TextType.BOLD, None),
            TextNode(" text", TextType.PLAIN, None),
            TextNode("This also contains ", TextType.PLAIN, None),
            TextNode("bold", TextType.BOLD, None),
            TextNode(" text", TextType.PLAIN, None),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_node_types_one_call(self):
        node_1 = TextNode("This contains **bold** text", TextType.PLAIN)
        node_2 = TextNode("This one contains _italic_ text", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node_1, node_2], "**", TextType.BOLD)
        expected = [
            TextNode("This contains ", TextType.PLAIN, None),
            TextNode("bold", TextType.BOLD, None),
            TextNode(" text", TextType.PLAIN, None),
            TextNode("This one contains _italic_ text", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_node_types_multiple_call(self):
        node_1 = TextNode("This contains **bold** text", TextType.PLAIN)
        node_2 = TextNode("This one contains _italic_ text", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node_1, node_2], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        expected = [
            TextNode("This contains ", TextType.PLAIN, None),
            TextNode("bold", TextType.BOLD, None),
            TextNode(" text", TextType.PLAIN, None),
            TextNode("This one contains ", TextType.PLAIN, None),
            TextNode("italic", TextType.ITALIC, None),
            TextNode(" text", TextType.PLAIN, None),
        ]
        self.assertEqual(new_nodes, expected)

    def test_nested_inline(self):
        node = TextNode(
            "This contains **bold text with _italic_ text inside**", TextType.PLAIN
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This contains ", TextType.PLAIN, None),
            TextNode("bold text with _italic_ text inside", TextType.BOLD, None),
        ]
        self.assertEqual(new_nodes, expected)

    def test_empty_input_list(self):
        new_nodes = split_nodes_delimiter([], "`", TextType.CODE)
        self.assertEqual(new_nodes, [])

    def test_non_plain_nodes_passthrough(self):
        nodes = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, nodes)

    def test_unbalanced_double_star(self):
        node = TextNode("This text is **not valid markdown!", TextType.PLAIN)
        with self.assertRaises(ValueError):
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_unbalanced_backtick(self):
        node = TextNode("This has one `backtick", TextType.PLAIN)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_unbalanced_underscore(self):
        node = TextNode("This has one _underscore", TextType.PLAIN)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "_", TextType.ITALIC)

    def test_single_star_does_not_raise_for_bold_delimiter(self):
        node = TextNode("It costs $5* per item", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("It costs $5* per item", TextType.PLAIN)])
