import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):

        # no properties
        html_node = HTMLNode()
        self.assertEqual(html_node.props_to_html(), '')

        # empty props
        html_node = HTMLNode(props = {})
        self.assertEqual(html_node.props_to_html(), '')

        # valid props
        html_node = HTMLNode(
            props = {
                "href": "https://www.google.com",
                "target": "_blank"
            }
        )
        self.assertEqual(html_node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_validate(self):
        # set neither value nor children
        html_node = HTMLNode()
        self.assertEqual(html_node.validate(), False)

        # set vale
        html_node = HTMLNode(value="some text")
        self.assertEqual(html_node.validate(), True)

        # set children
        html_node = HTMLNode(children=[HTMLNode(), HTMLNode()])
        self.assertEqual(html_node.validate(), True)

        # set empty children
        html_node = HTMLNode(children=[])
        self.assertEqual(html_node.validate(), True)

        # set both
        html_node = HTMLNode(value="some text", children=[HTMLNode(), HTMLNode()])
        self.assertEqual(html_node.validate(), True)
