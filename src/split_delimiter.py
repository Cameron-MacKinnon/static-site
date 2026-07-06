from src.textnode import TextNode, TextType


def check_delimiter_balance(text: str, delimiter: str):
    """Raises an error if the number of delimiters in a given string is odd"""

    if text.count(delimiter) % 2 != 0:
        raise ValueError(f'mismatched delimiter "{delimiter}" detected')


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    """Accepts a list of nodes and a delimiter, parses each node's text and
    splits it into several nodes where applicable (delimited text results in a
    node of the passed text_type, whereas all other text chunks become plain
    text nodes)"""
    new_nodes = []

    for node in old_nodes:
        # if an "old node" is not a TextType.TEXT type, just add it
        # to the new list as-is,we only attempt to split "text" type
        # objects (not bold, italic, etc).
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        # check that the text is syntactically correct markdown, if
        # it contains an uneven number of delimiters then it can't
        # be reliably interpreted
        check_delimiter_balance(node.text, delimiter)

        # split the node's text on the desired delimiter then create
        # new nodes accordingly
        sections = node.text.split(delimiter)
        for index, section in enumerate(sections):
            # non-special sections will always fall on even indexes,
            # the .split() method enforces this (if the string starts with
            # the delimiter - an empty string will be index 0). The second
            # condition filters out such instances where the section would
            # be an empty string
            if index % 2 == 0 and len(section) != 0:
                new_nodes.append(TextNode(section, TextType.PLAIN))
            # by that same logic, all special sections will fall on
            # odd indicies - these should never be blank but better safe
            # than sorry (probably)
            elif index % 2 != 0 and section:
                new_nodes.append(TextNode(section, text_type))

    return new_nodes
