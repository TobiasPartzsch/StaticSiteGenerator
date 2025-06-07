from markdown_blocks import BlockType


def extract_title(markdown: str) -> str:
    h1 = f"{BlockType.HEADING} "
    for line in markdown.split('\n'):
        if line.startswith(h1):
            return line[2:]
    raise ValueError(f"No first-level heading found in {"\n".join(markdown.split('\n'))}")

def generate_page():
    pass