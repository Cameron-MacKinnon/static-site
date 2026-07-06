import json

import src.htmlnode as htmlnode
from src.leafnode import LeafNode


class ParentNode(htmlnode.HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__()
        self.tag = tag
        self.children = children
        self.props = props

    def __repr__(self):
        return json.dumps(
            {
                "tag": self.tag,
                "children": self.children,
                "props": self.props,
            },
            indent=2,
        )

    def to_html(self):
        # handle exceptional cases
        if not self.tag:
            raise ValueError("all parent nodes must have a tag")
        if not self.children:
            raise ValueError("all parent nodes must have at least one child")

        # open string add props if they exist
        if not self.props:
            html_string = f"<{self.tag}>"
        else:
            html_string = f"<{self.tag}{self.props_to_html()}>"

        # build node contents
        for child in self.children:
            html_string += child.to_html()

        # close html string
        html_string += f"</{self.tag}>"
        return html_string
