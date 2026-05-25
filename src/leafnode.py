import json

import htmlnode


class LeafNode(htmlnode.HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__()
        self.tag = tag
        self.value = value
        self.props = props

    def __repr__(self):
        return json.dumps(
            {
                "tag": self.tag,
                "value": self.value,
                "props": self.props,
            },
            indent=2,
        )

    def to_html(self):
        # handle exceptional casess
        if not self.value:
            raise ValueError("all leaf nodes must have a value")
        if not self.tag:
            return self.value

        # handle basic tag with no properties
        if not self.props:
            return f"<{self.tag}>{self.value}</{self.tag}>"

        # inject props into string if present
        html_string = f"<{self.tag}"
        for k, v in self.props.items():
            html_string += f' {k}="{v}"'
        html_string += f">{self.value}</{self.tag}>"
        return html_string
