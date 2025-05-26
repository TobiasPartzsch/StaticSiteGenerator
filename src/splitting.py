from itertools import chain
import re
from typing import Callable, Iterable
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

UNMATCHED_DELIMITER_ERROR_MSG = "Unmatched delimters {delimiter} in text {text}"

def split_node_on_delimiter(text_node: TextNode, delimiter: str, text_type: TextType) -> list[TextNode]:
    if text_node.text_type != TextType.TEXT:
        return [text_node]
    parts = text_node.text.split(delimiter)
    if not len(parts) % 2:  # even parts mean unmatched delimiters
        raise ValueError(UNMATCHED_DELIMITER_ERROR_MSG.format(delimiter=delimiter, text=text_node.text))
    return [
        TextNode(part, TextType.TEXT if i % 2 == 0 else text_type)
        for i, part in enumerate(parts)
    ]

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return list(re.findall(r"!\[(?P<text>[^\]]+)\]\((?P<link>[^\)]+)\)", text))

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return list(re.findall(r"(?<!!)\[(?P<text>[^\]]+)\]\((?P<link>[^\)]+)\)", text))


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes(old_nodes, extract_markdown_images, TextType.IMAGE)

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes(old_nodes, extract_markdown_links, TextType.LINK)

def split_nodes(
        old_nodes: list[TextNode],
        extraction_function: Callable[[str], list[tuple[str, str]]],
        text_type: TextType,
        ) -> list[TextNode]:
    nodes_to_process = old_nodes.copy()
    processed_nodes: list[TextNode] = []
    while len(nodes_to_process):
        current_node = nodes_to_process.pop(0)
        images = extraction_function(current_node.text)
        if not images:
            processed_nodes.append(current_node)
            continue
        alt, link = images[0]  # TODO: handle all at once
        head, tail = current_node.text.split(f"{'!' if text_type == TextType.IMAGE else ''}[{alt}]({link})", 1)
        if head:
            processed_nodes.append(TextNode(head, TextType.TEXT))
        processed_nodes.append(TextNode(alt, text_type, link))
        if tail:
            nodes_to_process.insert(0, TextNode(tail, TextType.TEXT))
    return processed_nodes
