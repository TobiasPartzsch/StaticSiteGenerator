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

