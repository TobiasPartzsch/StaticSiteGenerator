import unittest
from splitting import UNMATCHED_DELIMITER_ERROR_MSG, extract_markdown_images, extract_markdown_links, markdown_to_blocks, split_node_on_delimiter, split_nodes_image, text_to_textnodes
from testscenarios import StringConversionScenario, run_subtest_cases
from textnode import DELIMITERS, TextNode, TextType


class TestSplitting(unittest.TestCase):
    def test_split_node_on_delimiter(self):
        for text_type, delimiter in DELIMITERS.items():
            with self.subTest(text_type=text_type, delimiter=delimiter):
                # No delimiter present (should remain unchanged)
                text = "Node without delimiters shouldn't change!"
                text_node = TextNode(text, TextType.TEXT)
                self.assertEqual(
                    split_node_on_delimiter(text_node, delimiter, text_type),
                    [text_node]
                )

                # Single pair of delimiters (should split into three nodes)
                text = f"Single pair of {delimiter}delimiters{delimiter} (should split into three nodes)"
                text_node = TextNode(text, TextType.TEXT)
                split_list = split_node_on_delimiter(text_node, delimiter, text_type)
                self.assertEqual(
                    len(split_list),
                    3
                )

                # Multiple pairs (should alternate correctly)
                text = f"Multiple {delimiter}pairs{delimiter} ({delimiter}should{delimiter} alternate {delimiter}correctly{delimiter})"
                text_node = TextNode(text, TextType.TEXT)
                split_list = split_node_on_delimiter(text_node, delimiter, text_type)
                self.assertEqual(
                    len(split_list),
                    7
                )
                for idx, node in enumerate(split_list):
                    if idx % 2:
                        self.assertEqual(node.text_type, text_type)
                    else:
                        self.assertEqual(node.text_type, TextType.TEXT)

                # Umatched delimiter (should raise an exception)
                invalid_node = TextNode(f"I am invalid! {delimiter} because I don't close", TextType.TEXT)
                with self.assertRaises(ValueError) as cm:
                    split_node_on_delimiter(invalid_node, delimiter, text_type)
                self.assertEqual(str(cm.exception), UNMATCHED_DELIMITER_ERROR_MSG.format(delimiter=delimiter, text=invalid_node.text))

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

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

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_to_textnodes(text)
        )

    def test_markdown_to_blocks(self):
        SplitTestScenario = StringConversionScenario[list[str]]

        test_cases = {
            "empty_string": SplitTestScenario("", []),
            "whitespace_blocks": SplitTestScenario("block1\n\n   \n\nblock2", ["block1", "block2"]),
            "bolded pararaph": SplitTestScenario(
                """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
""",
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            ),
            "starts with newline": SplitTestScenario(
                """

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
""",
                [
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line"
                ],
            ),
            "ends with newline": SplitTestScenario(
                """
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


""",
                [
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                ],
            ),
            "multiple_blank_lines": SplitTestScenario("block1\n\n\n\n\nblock2", ["block1", "block2"]),
            "whitespace_only": SplitTestScenario("   \n\n   ", []),
        }
        
        run_subtest_cases(self, markdown_to_blocks, test_cases)


    # Multiple consecutive blank lines between blocks?
    # A string with no blocks at all?
