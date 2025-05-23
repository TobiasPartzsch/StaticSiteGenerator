from dataclasses import dataclass
from enum import StrEnum
from typing import Optional

from leafnode import LeafNode

class TextType(StrEnum):
    NORMAL = "Normal text"
    BOLD = "**Bold text**"
    ITALIC = "_Italic text_"
    CODE = "`Code text`"
    LINK = "Links, in this format: [anchor text](url)"
    IMAGE = "Images, in this format: ![alt text](url)"

class Tags(StrEnum):
    NORMAL = ''
    BOLD = "b"
    ITALIC = "i"
    CODE = "code"
    LINK = "a"
    IMAGE = "img"


@dataclass
class TextNode:
    """Representation of inline text.
    """

    """The text content of the node"""
    text: str

    """The type of text this node contains, which is a member of the TextType enum."""
    text_type: TextType

    """The URL of the link or image, if the text is a link. Default to None if nothing is passed in."""
    url: Optional[str] = None

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode.text_only(text_node.text)
        case TextType.BOLD:
            return LeafNode(str(Tags.BOLD), text_node.text)
        case TextType.ITALIC:
            return LeafNode(str(Tags.ITALIC), text_node.text)
        case TextType.CODE:
            return LeafNode(str(Tags.CODE),text_node.text)
        case TextType.LINK:
            return LeafNode(str(Tags.LINK), text_node.text, {'href': text_node.url or ''})
        case TextType.IMAGE:
            return LeafNode(str(Tags.IMAGE), '', {"src": text_node.url or '', "alt": text_node.text or ''})
        case _:
            raise ValueError(f"Unkown text type: {text_node.text_type}")