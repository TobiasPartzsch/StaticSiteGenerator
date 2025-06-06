from dataclasses import dataclass
from typing import Optional
import unittest

from leafnode import LeafNode
from textnode import Tags, TextNode, TextType, text_node_to_html_node


class TestBlockToBlockType(unittest.TestCase):
    def test_eq(self):
        test_name = "This is a text node"
        test_type = TextType.TEXT
        node = TextNode(test_name, test_type)
        node2 = TextNode(test_name, test_type)
        self.assertEqual(node, node2)

        # different text name
        test_name = "This is a text node"
        test_type = TextType.BOLD
        node = TextNode(test_name, test_type)
        node2 = TextNode(test_name * 2, test_type)
        self.assertNotEqual(node, node2)

        # different text type
        test_name = "This is a text node"
        test_type1 = TextType.BOLD
        test_type2 = TextType.LINK
        node = TextNode(test_name, test_type1)
        node2 = TextNode(test_name, test_type2)
        self.assertNotEqual(node, node2)

        # explicit equal url
        test_name = "This is a text node"
        test_type = TextType.BOLD
        url = "some url"
        node = TextNode(test_name, test_type, url)
        node2 = TextNode(test_name, test_type, url)
        self.assertEqual(node, node2)

        # explicit different url
        test_name = "This is a text node"
        test_type = TextType.BOLD
        url1 = "some url"
        url2 = "some other url"
        node = TextNode(test_name, test_type, url1)
        node2 = TextNode(test_name, test_type, url2)
        self.assertNotEqual(node, node2)

    def test_text_node_to_HTML_node(self):
        test_cases:tuple["TestCase", ...] = (
            TestCase(
                input=Input(text="This is a text node", text_type=TextType.TEXT),
            ),
            TestCase(
                input=Input(text="This is a bold text node", text_type=TextType.BOLD),
            ),
            TestCase(
                input=Input(text="This is an italic text node", text_type=TextType.ITALIC),
            ),
            TestCase(
                input=Input(text="This is an code text node", text_type=TextType.CODE),
            ),
            TestCase(
                input=Input(text="This is an link text node", text_type=TextType.LINK, url="some url"),
            ),
            TestCase(
                input=Input(text="This is an image text node", text_type=TextType.IMAGE, url="some url"),
            ),
        )

        # Get attributes once from the class and ignore protected attributes
        html_attrs = {attr for attr in dir(LeafNode) if not attr.startswith('_')}
        expected_attrs = {attr for attr in dir(Expected) if not attr.startswith('_')}
        # Expected should be a subset of LeafNode's attributes
        self.assertTrue(
            expected_attrs.issubset(html_attrs), 
            "Expected attributes should be available on LeafNode"
            )

        for test_case in test_cases:
            with self.subTest(node_type=test_case.input.text_type):
                # Convert the input to a TextNode, then to HTMLNode
                text_node = TextNode(
                    test_case.input.text,
                    test_case.input.text_type,
                    test_case.input.url
                    )
                html_node = text_node_to_html_node(text_node)
                
                # Get the expected result from your computed property
                expected = test_case.expected
                
                # Assert they match
                self.assertEqual(html_node.tag, expected.tag)
                self.assertEqual(html_node.value, expected.value)
                self.assertEqual(html_node.props, expected.props)

    def test_unknown_text_type_raises_exception(self):
        invalid_node = TextNode("I am invalid!", 'haha') # type: ignore
        with self.assertRaises(ValueError) as cm:
            text_node_to_html_node(invalid_node)
        self.assertEqual(str(cm.exception), f"Unkown text type: {invalid_node.text_type}")


@dataclass
class Input:
    text: str
    text_type: TextType
    url: Optional[str] = None

@dataclass
class Expected:
    tag: Optional[str]
    value: str
    props: Optional[dict[str, str]] = None

@dataclass
class TestCase:
    input: Input
    # expected_props: Optional[dict[str, str]] = None

    @property
    def expected(self):
        return Expected(
            tag=self.expected_tag,
            value=self.expected_value,
            props=self.expected_props
            )
    
    @property
    def expected_tag(self):
        return Tags[self.input.text_type.name].value

    @property
    def expected_value(self) -> str:
        # Images use empty string, all other types use the input text
        if self.input.text_type == TextType.IMAGE:
            return ""
        return self.input.text

    @property
    def expected_props(self) -> Optional[dict[str, str]]:
        match self.input.text_type:
            case TextType.LINK:
                return {"href": self.input.url or ''}
            case TextType.IMAGE:
                return {"src": self.input.url or '', "alt": self.input.text}
            case _:
                return None


if __name__ == "__main__":
    unittest.main()