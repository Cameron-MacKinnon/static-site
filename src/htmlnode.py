import json


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return json.dumps(
            {
                "tag": self.tag,
                "value": self.value,
                "children": self.children,
                "props": self.props,
            },
            indent=2,
        )

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        output = ""
        if not self.props:
            return output
        for k, v in self.props.items():
            output += f' {k}="{v}"'
        return output
