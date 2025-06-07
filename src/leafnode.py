from typing import Optional

from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
            self,
            tag: str,
            value: str,
            props: Optional[dict[str, str]] = None
        ):
        super().__init__(tag=tag, children=None, value=value, props=props)

    def __repr__(self):
        return (f"LeafNode(tag={repr(self.tag)}, value={repr(self.value)}, "
                f"props={repr(self.props)})")

    @classmethod
    def text_only(cls, value: str):
        return cls(tag='', value=value)

    def to_html(self):
        if self.value is None:
            # If the leaf node has no value, it should raise a ValueError. All leaf nodes must have a value.
            raise ValueError("All leaf nodes must have a value.")
        if not self.tag:
            # if there is no tag (e.g. it's an empty string), the value should be returned as raw text.
            return str(self.value)
        # Otherwise, it should render an HTML tag
        if self.props:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"
