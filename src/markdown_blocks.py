from enum import StrEnum

from htmlnode import HTMLNode, Tags
from leafnode import LeafNode
from parentnode import ParentNode
from splitting import markdown_to_blocks, text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


MAX_HEADER_LEVELS = 6

class BlockType(StrEnum):
    PARAGRAPH = ''
    HEADING = '#'
    CODE = '`'
    QUOTE = '>'
    UNORDERED_LIST = '-'
    ORDERED_LIST = '1'


def block_to_block_type(block: str) -> BlockType:
    if not block:
        # empty paragraph
        return BlockType.PARAGRAPH

    match block[0]:
        case BlockType.HEADING:
            return BlockType.HEADING if __is_heading(block) else BlockType.PARAGRAPH
        case BlockType.CODE:
            return BlockType.CODE if __is_code(block) else BlockType.PARAGRAPH
        case BlockType.QUOTE:
            return BlockType.QUOTE if __is_quote(block) else BlockType.PARAGRAPH
        case BlockType.UNORDERED_LIST:
            return BlockType.UNORDERED_LIST if __is_unordered_list(block) else BlockType.PARAGRAPH
        case BlockType.ORDERED_LIST:
            return BlockType.ORDERED_LIST if __is_ordered_list(block) else BlockType.PARAGRAPH
        case _:
            block_type = BlockType.PARAGRAPH

    return block_type

def __is_heading(block: str) -> bool:
    if "\n" in block:
        # headings must be single line
        return False
    if len(block) < 3:
        return False
    idx = 1
    while idx < len(block) and idx < MAX_HEADER_LEVELS and block[idx] == BlockType.HEADING:
        idx +=1
    if len(block) < idx + 2:
        # need at least two more characters if this is a heading
        return False
    return block[idx].isspace() and not block[idx + 1].isspace()

def __is_code(block: str) -> bool:
    if len(block) < 6:
        # codeblocks need at least 6 characters
        return False
    return block[:3] == block[-3:] == BlockType.CODE * 3

def __is_quote(block: str) -> bool:
    for line in block.split('\n'):
        if not line.startswith(BlockType.QUOTE):
            return False
    return True

def __is_unordered_list(block: str) -> bool:
    for line in block.split('\n'):
        if not line.startswith(BlockType.UNORDERED_LIST + ' '):
            return False
    return True

def __is_ordered_list(block: str) -> bool:
    for idx, line in enumerate(block.split('\n'), start=1):
        if not line.startswith(f"{idx}. "):
            return False
    return True

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children: list[HTMLNode] = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode(Tags.div, children, None)


def block_to_html_node(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return olist_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return ulist_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case _: # This is the catch-all case
            raise ValueError(f"invalid block type: {block_type}")


def text_to_children(text: str) -> list[LeafNode]:
    text_nodes = text_to_textnodes(text)
    children: list[LeafNode] = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode(Tags.p, children)


def heading_to_html_node(block: str) -> ParentNode:
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block: str) -> ParentNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode(Tags.code, [child])
    return ParentNode(Tags.pre, [code])


def olist_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    html_items: list[ParentNode] = []
    for item in items:
        text = item[3:].strip()
        children = text_to_children(text)
        html_items.append(ParentNode(Tags.li, children))
    return ParentNode(Tags.ol, html_items)


def ulist_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    html_items: list[ParentNode] = []
    for item in items:
        text = item[2:].strip()
        children = text_to_children(text)
        html_items.append(ParentNode(Tags.li, children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    new_lines = [line.lstrip(">").strip() for line in lines]
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode(Tags.blockquote, children)
