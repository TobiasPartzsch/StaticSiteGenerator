import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        test_name = "This is a text node"
        test_type = TextType.BOLD
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

if __name__ == "__main__":
    unittest.main()