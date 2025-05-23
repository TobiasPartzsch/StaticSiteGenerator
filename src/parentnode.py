from typing import Optional

from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
            self,
            tag: str,
            children: list[HTMLNode],
            props: Optional[dict[str, str]] = None
        ):
        super().__init__(tag=tag, children=children, value=None, props=props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("Parent nodes need a tag!")
        if self.children is None:
            raise ValueError("Parent nodes need children (even if the list is empty)")
        return f"<{self.tag}>{''.join(child.to_html() for child in self.children)}</{self.tag}>"
