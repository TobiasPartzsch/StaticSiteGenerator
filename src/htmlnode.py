from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Optional, Sequence

# Define the StrEnum for HTML tags
class Tags(StrEnum):
    p = auto()
    h1 = auto()
    h2 = auto()
    h3 = auto()
    h4 = auto()
    h5 = auto()
    h6 = auto()
    pre = auto()
    code = auto()
    blockquote = auto()
    ul = auto()
    ol = auto()
    li = auto()
    b = auto()
    i = auto()
    a = auto()
    img = auto()
    div = auto()


@dataclass
class HTMLNode:
    """- A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)"""
    tag: Optional[str] = None

    """A string representing the value of the HTML tag (e.g. the text inside a paragraph)"""
    value: Optional[str] = None

    """A list of HTMLNode objects representing the children of this node"""
    children: Optional[Sequence["HTMLNode"]] = None

    """A dictionary of key-value pairs representing the attributes of the HTML tag.
    For example, a link (<a> tag) might have {"href": "https://www.google.com"}"""
    props: Optional[dict[str, str]] = None

    def __eq__(self, other: object):
        if not isinstance(other, HTMLNode):
            # If 'other' is not an HTMLNode, they are not equal
            return False

        # Compare the attributes. If any differ, they are not equal.
        # Include checks for children being None vs empty list if necessary based on your implementation
        if self.tag != other.tag:
            # Optional: print a specific message about the difference
            # print(f"HTMLNode equality check failed: Tags differ - self.tag='{self.tag}', other.tag='{other.tag}'")
            return False
        if self.value != other.value:
            # Optional: print a specific message about the difference
            # print(f"HTMLNode equality check failed: Values differ - self.value='{self.value}', other.value='{other.value}'")
            return False
        # Comparing lists of children needs careful handling if order matters or if comparing None vs empty list
        if (self.children is None and other.children is not None) or \
           (self.children is not None and other.children is None) or \
           (self.children is not None and other.children is not None and list(self.children) != list(other.children)):
             # Optional: print a specific message about the difference
            #  print(f"HTMLNode equality check failed: Children differ - self.children={self.children}, other.children={other.children}")
             return False
        if self.props != other.props:
            # Optional: print a specific message about the difference
            # print(f"HTMLNode equality check failed: Props differ - self.props={self.props}, other.props={other.props}")
            return False

        # If all attributes are equal, the nodes are equal
        return True

    def __repr__(self):
        # This method returns a string that is a clear and unambiguous
        # representation of the object, ideally one that could be used
        # to recreate the object if possible.

        # It should show the key attributes: tag, value, children, and props.
        # We use f-strings for easy formatting.

        # Handle children carefully as they are a list of other HTMLNodes
        children_repr = "None"
        if self.children is not None:
            # Join the repr of each child for the string representation
            children_repr = "[" + ", ".join(repr(child) for child in self.children) + "]"

        # Handle props similarly as a dictionary
        props_repr = "None"
        if self.props is not None:
            # Directly represent the dictionary
            props_repr = repr(self.props)


        return (f"HTMLNode(tag={repr(self.tag)}, value={repr(self.value)}, "
                f"children={children_repr}, props={props_repr})")

    def to_html(self)-> str:
        raise NotImplementedError("Child classes will override this method to render themselves as HTML")
    
    def props_to_html(self) -> str:
        if not self.props:
            return ""
        return f" {' '.join(k + '=\"' + v + '\"' for (k, v) in self.props.items())}"
    
    def validate(self) -> bool:
        return self.value is not None or self.children is not None
    