import unittest
from splitting import UNMATCHED_DELIMITER_ERROR_MSG, extract_markdown_images, extract_markdown_links, split_nodes_image
from textnode import DELIMITERS, TextNode, TextType, text_node_to_html_node


class TestSplitting(unittest.TestCase):
    def test_split_node_on_delimiter(self):
        for text_type, delimiter in DELIMITERS.items():
            with self.subTest(text_type=text_type, delimiter=delimiter):
                # No delimiter present (should remain unchanged)

                # Single pair of delimiters (should split into three nodes)

                # Multiple pairs (should alternate correctly)

                # Umatched delimiter (should raise an exception)
                invalid_node = TextNode("I am invalid! {delimiter} because I don't close", text_type)
                with self.assertRaises(ValueError) as cm:
                    text_node_to_html_node(invalid_node)
                self.assertEqual(str(cm.exception), UNMATCHED_DELIMITER_ERROR_MSG.format(delimiter=delimiter, text=invalid_node.text))

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )