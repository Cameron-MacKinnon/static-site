from htmlnode import HTMLNode
from textnode import TextNode, TextType


def main():
    # dummy TextNode for testing
    new_node = TextNode("Here's a link", TextType.LINK, "https://www.boot.dev")
    print(new_node)

    # dummy HTMLNode for testing
    new_node = HTMLNode(
        "<p>",
        "foobar",
        None,
        {
            "href": "https://www.google.com",
            "target": "_blank",
        },
    )
    print(new_node)


if __name__ == "__main__":
    main()
