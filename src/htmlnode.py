from dataclasses import dataclass
from typing import Optional


@dataclass
class HTMLNode:
    """- A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)"""
    tag: Optional[str] = None

    """A string representing the value of the HTML tag (e.g. the text inside a paragraph)"""
    value: Optional[str] = None

    """A list of HTMLNode objects representing the children of this node"""
    children: Optional[list["HTMLNode"]] = None

    """A dictionary of key-value pairs representing the attributes of the HTML tag.
    For example, a link (<a> tag) might have {"href": "https://www.google.com"}"""
    props: Optional[dict[str, str]] = None

    def to_html(self)-> str:
        raise NotImplementedError("Child classes will override this method to render themselves as HTML")
    
    def props_to_html(self) -> str:
        if not self.props:
            return ""
        return f" {' '.join(k + '=\"' + v + '\"' for (k, v) in self.props.items())}"
    
    def validate(self) -> bool:
        return self.value is not None or self.children is not None
    