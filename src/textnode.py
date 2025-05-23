from dataclasses import dataclass
from enum import Enum
from typing import Optional

class TextType(Enum):
    NORMAL = "Normal text"
    BOLD = "**Bold text**"
    ITALIC = "_Italic text_"
    CODE = "`Code text`"
    LINK = "Links, in this format: [anchor text](url)"
    IMAGE = "Images, in this format: ![alt text](url)"


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
    