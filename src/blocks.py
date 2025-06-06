from enum import StrEnum


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
        block_type = BlockType.PARAGRAPH

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
    while block[idx] == BlockType.HEADING and idx < MAX_HEADER_LEVELS:
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
