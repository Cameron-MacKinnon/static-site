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
