from dataclasses import dataclass
from enum import StrEnum
from itertools import chain
from typing import Iterable, Optional

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

DELIMITERS = {
    TextType.BOLD: "**",
    TextType.ITALIC: "_",
    TextType.CODE: "`",
}


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

def split_nodes_delimiter(old_nodes:list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    """Split plain text depending on delimiter. Other types of TextNode won't be changed.
    """
    return list(
        chain.from_iterable(
            (
                (node,) if node.text_type != TextType.NORMAL
                else split_node_on_delimiter(node, delimiter, text_type)
                for node in old_nodes
            )
        )
    )

UNMATCHED_DELIMITER_ERROR_MSG = "Unmatched delimters {delimiter} in text {text_node.text}"

def split_node_on_delimiter(text_node: TextNode, delimiter: str, text_type: TextType) -> Iterable["TextNode"]:
    if text_node.text_type != TextType.NORMAL:
        return (text_node, )
    parts = text_node.text.split(delimiter)
    if not len(parts) % 2:  # even parts mean unmatched delimiters
        raise ValueError(UNMATCHED_DELIMITER_ERROR_MSG.format(delimiter=delimiter, text=text_node.text))
    return (
        TextNode(part, TextType.NORMAL if i % 2 == 0 else text_type)
        for i, part in enumerate(parts)
    )
