from itertools import chain
import re
from typing import Iterable
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: Iterable[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    """Split plain text depending on delimiter. Other types of TextNode won't be changed.
    """
    return list(
        chain.from_iterable(
            (
                (node,) if node.text_type != TextType.TEXT
                else split_node_on_delimiter(node, delimiter, text_type)
                for node in old_nodes
            )
        )
    )

UNMATCHED_DELIMITER_ERROR_MSG = "Unmatched delimters {delimiter} in text {text_node.text}"

def split_node_on_delimiter(text_node: TextNode, delimiter: str, text_type: TextType) -> Iterable["TextNode"]:
    if text_node.text_type != TextType.TEXT:
        return (text_node, )
    parts = text_node.text.split(delimiter)
    print(parts)
    if not len(parts) % 2:  # even parts mean unmatched delimiters
        raise ValueError(UNMATCHED_DELIMITER_ERROR_MSG.format(delimiter=delimiter, text=text_node.text))
    return (
        TextNode(part, TextType.TEXT if i % 2 == 0 else text_type)
        for i, part in enumerate(parts)
    )

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall("", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall("", text)


def split_nodes_image(old_nodes: Iterable[TextNode]) -> list[TextNode]:
    pass

def split_nodes_link(old_nodes: Iterable[TextNode]) -> list[TextNode]:
    pass