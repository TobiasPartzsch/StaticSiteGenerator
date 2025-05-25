import unittest
from splitting import UNMATCHED_DELIMITER_ERROR_MSG
from textnode import DELIMITERS, TextNode, text_node_to_html_node


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
