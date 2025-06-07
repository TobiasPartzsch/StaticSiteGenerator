from typing import Optional, Sequence

from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
            self,
            tag: str,
            children: Sequence[HTMLNode],
            props: Optional[dict[str, str]] = None
        ):
        super().__init__(tag=tag, children=children, value=None, props=props)

    def __repr__(self):
        # Representation should focus on the ParentNode's key attributes: tag and children.
        # Value is typically None for a ParentNode, and props might be included if important.

        # Handle children carefully as they are a list of other HTMLNodes
        children_repr = "None"
        if self.children is not None:
            # Join the repr of each child for the string representation
            children_repr = "[" + ", ".join(repr(child) for child in self.children) + "]"

        # Handle props similarly as a dictionary, or omit if usually None
        props_repr = "None"
        if self.props is not None:
            props_repr = repr(self.props)

        # Return a string representing the ParentNode
        # We include the tag and children, and optionally props
        return (f"ParentNode(tag={repr(self.tag)}, children={children_repr}, "
                f"props={props_repr})")

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("Parent nodes need a tag!")
        if self.children is None:
            raise ValueError("Parent nodes need children (even if the list is empty)")
        return f"<{self.tag}>{''.join(child.to_html() for child in self.children)}</{self.tag}>"

