from enum import Enum


class TextType(Enum):
    """Represents all valid inline text types"""

    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(self, other):
            return False
        if other.text != self.text:
            return False
        elif other.text_type != self.text_type:
            return False
        elif other.url != self.url:
            return False
        return True

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
