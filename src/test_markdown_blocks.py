import unittest

from htmlnode import HTMLNode, Tags
from leafnode import LeafNode
from markdown_blocks import BlockType, block_to_block_type, block_to_html_node, text_to_children
from parentnode import ParentNode
from testscenarios import StringConversionScenario, run_subtest_cases


class TestBlockToBlockType(unittest.TestCase):
    BlockTypeTestScenario = StringConversionScenario[BlockType]

    def test_headings(self):
        test_cases = {
            f"h{level}": self.BlockTypeTestScenario(
                input=f"{'#' * level} Heading {level}",
                expected=BlockType.HEADING
            )
            for level in range(1, 7)
        }

        test_cases.update(
            {
                "heading with extra text": self.BlockTypeTestScenario("### Hello World!", BlockType.HEADING),
                "not heading no space": self.BlockTypeTestScenario("#NoSpace", BlockType.PARAGRAPH),
                "not heading too many": self.BlockTypeTestScenario("####### Too many hashes", BlockType.PARAGRAPH),
                "not heading zero": self.BlockTypeTestScenario("Heading without hash", BlockType.PARAGRAPH),
            }
        )
        run_subtest_cases(self, block_to_block_type, test_cases)

    def test_code_blocks(self):
        test_cases = {
            "simple code": self.BlockTypeTestScenario("```\nprint('hello')\n```", BlockType.CODE),
            "multiline code": self.BlockTypeTestScenario("```\nline1\nline2\nline3\n```", BlockType.CODE),
            "empty code": self.BlockTypeTestScenario("```\n```", BlockType.CODE),
            "not code missing end": self.BlockTypeTestScenario("```\ncode without end", BlockType.PARAGRAPH),
            "not code missing start": self.BlockTypeTestScenario("code without start\n```", BlockType.PARAGRAPH),
        }
        run_subtest_cases(self, block_to_block_type, test_cases)

    def test_quote_blocks(self):
        test_cases = {
            "simple quote": self.BlockTypeTestScenario("> Don't worry, be happy", BlockType.QUOTE),
            "multiline quote": self.BlockTypeTestScenario("> Line 1\n> Line 2", BlockType.QUOTE),
            "empty quote": self.BlockTypeTestScenario(">", BlockType.QUOTE),  # Test this edge case
            "quote with space": self.BlockTypeTestScenario("> ", BlockType.QUOTE),  # And this one
            "mixed invalid": self.BlockTypeTestScenario("> Quote line\nNot quote", BlockType.PARAGRAPH),
            "missing gt": self.BlockTypeTestScenario("Not a quote", BlockType.PARAGRAPH),
        }
        run_subtest_cases(self, block_to_block_type, test_cases)

    def test_unordered_list_blocks(self):
        test_cases = {
            "single item": self.BlockTypeTestScenario("- Item 1", BlockType.UNORDERED_LIST),
            "multiple items": self.BlockTypeTestScenario("- Item 1\n- Item 2\n- Item 3", BlockType.UNORDERED_LIST),
            "with spaces": self.BlockTypeTestScenario("-   Item with extra spaces", BlockType.UNORDERED_LIST),
            "empty item": self.BlockTypeTestScenario("- ", BlockType.UNORDERED_LIST),
            "no space after dash": self.BlockTypeTestScenario("-Item", BlockType.PARAGRAPH),
            "mixed valid invalid": self.BlockTypeTestScenario("- Item 1\nNot a list item", BlockType.PARAGRAPH),
            "some lines missing dash": self.BlockTypeTestScenario("- Item 1\n- Item 2\nPlain text", BlockType.PARAGRAPH),
            "starts with text": self.BlockTypeTestScenario("Not a list\n- Item 1", BlockType.PARAGRAPH),
        }        
        run_subtest_cases(self, block_to_block_type, test_cases)

    def test_ordered_lists(self):
        test_cases = {
            "single item": self.BlockTypeTestScenario("1. First item", BlockType.ORDERED_LIST),
            "multiple items": self.BlockTypeTestScenario("1. First\n2. Second\n3. Third", BlockType.ORDERED_LIST),
            "with extra spaces": self.BlockTypeTestScenario("1.   Item with spaces", BlockType.ORDERED_LIST),
            "empty item": self.BlockTypeTestScenario("1. ", BlockType.ORDERED_LIST),
            
            # Invalid cases - should be PARAGRAPH
            "starts with 0": self.BlockTypeTestScenario("0. Zero start", BlockType.PARAGRAPH),
            "starts with 2": self.BlockTypeTestScenario("2. Wrong start", BlockType.PARAGRAPH),
            "skips number": self.BlockTypeTestScenario("1. First\n3. Skipped two", BlockType.PARAGRAPH),
            "wrong sequence": self.BlockTypeTestScenario("1. First\n3. Wrong\n2. Wrong", BlockType.PARAGRAPH),
            "no space after period": self.BlockTypeTestScenario("1.NoSpace", BlockType.PARAGRAPH),
            "no period": self.BlockTypeTestScenario("1 No period", BlockType.PARAGRAPH),
            "mixed with text": self.BlockTypeTestScenario("1. First\nPlain text", BlockType.PARAGRAPH),
            "some lines not numbered": self.BlockTypeTestScenario("1. First\n2. Second\n- Not numbered", BlockType.PARAGRAPH),
            "double digits": self.BlockTypeTestScenario("1. First\n2. Second\n10. Jump to ten", BlockType.PARAGRAPH),
        }
        run_subtest_cases(self, block_to_block_type, test_cases)

    def test_paragraphs(self):
        test_cases = {
            "simple text": self.BlockTypeTestScenario("Just some plain text", BlockType.PARAGRAPH),
            "multiline text": self.BlockTypeTestScenario("Line 1\nLine 2\nLine 3", BlockType.PARAGRAPH),
            "text with markdown": self.BlockTypeTestScenario("This has **bold** and *italic* text", BlockType.PARAGRAPH),
            "numbers and symbols": self.BlockTypeTestScenario("Some text with 123 and @#$ symbols", BlockType.PARAGRAPH),
            "special characters": self.BlockTypeTestScenario("Text with ñ, é, ü, and 中文", BlockType.PARAGRAPH),
            "punctuation heavy": self.BlockTypeTestScenario("Lots of punctuation!!! What? Yes... (maybe)", BlockType.PARAGRAPH),
            "urls and emails": self.BlockTypeTestScenario("Visit https://example.com or email test@example.com", BlockType.PARAGRAPH),
            "mixed symbols": self.BlockTypeTestScenario("$100 + 50% = good deal & more @ store", BlockType.PARAGRAPH),
            "almost heading": self.BlockTypeTestScenario("#but no space after", BlockType.PARAGRAPH),
            "almost list": self.BlockTypeTestScenario("- but\nno dash on second line", BlockType.PARAGRAPH),
            "almost code": self.BlockTypeTestScenario("```missing end", BlockType.PARAGRAPH),
            "empty string": self.BlockTypeTestScenario("", BlockType.PARAGRAPH),
            "just whitespace": self.BlockTypeTestScenario("   \t  ", BlockType.PARAGRAPH),  # If whitespace isn't stripped
        }
        run_subtest_cases(self, block_to_block_type, test_cases)


class TestMarkupToHTML(unittest.TestCase):
    HTMLTestScenario = StringConversionScenario[HTMLNode]

    def test_headings(self):
        heading_text_template = "Heading {level}"
        test_cases = {
            f"h{level} conversion": self.HTMLTestScenario(
                input=f"{'#' * level} {heading_text_template.format(level=level)}",
                expected=ParentNode(
                    f"h{level}",
                    text_to_children(heading_text_template.format(level=level))
                )
            )
            for level in range(1, 7)
        }
        extra_text = "Hello World!"
        no_space = "#NoSpace"
        too_many = "####### Too many hashes"
        no_hash = "Heading without hash"
        test_cases.update(
            {
                "heading with extra text": self.HTMLTestScenario(f"### {extra_text}", ParentNode(Tags.h3, text_to_children(extra_text))),
                "not heading no space": self.HTMLTestScenario(f"{no_space}", ParentNode(Tags.p, text_to_children(no_space))),
                "not heading too many": self.HTMLTestScenario(f"{too_many}", ParentNode(Tags.p, text_to_children(too_many))),
                "not heading zero": self.HTMLTestScenario(f"{no_hash}", ParentNode(Tags.p, text_to_children(no_hash))),
            }
        )
        run_subtest_cases(self, block_to_html_node, test_cases)

    def test_code_blocks(self):
        simple = "print('hello')\n"
        multiline = "line1\nline2\nline3\n"
        empty = ""
        # no_end = "```\ncode without end"
        # no_start = "code without start\n```"
        test_cases = {
            "simple code": self.HTMLTestScenario(
                f"```\n{simple}```",
                ParentNode(
                    Tags.pre,
                    [ParentNode(Tags.code, [LeafNode.text_only(simple)])]
                )
            ),
            "multiline code": self.HTMLTestScenario(
                f"```\n{multiline}```",
                ParentNode(
                    Tags.pre,
                    [ParentNode(Tags.code, [LeafNode.text_only(multiline)])]
                )
            ),
            "empty code": self.HTMLTestScenario(
                f"```\n{empty}```",
                ParentNode(
                    Tags.pre,
                    [ParentNode(Tags.code, [LeafNode.text_only(empty)])] # Empty string for empty code block
                )
            ),
            # TODO: make tests that raise errors possible
            # "not code missing end": self.HTMLTestScenario(
            #     f"{no_end}",
            #     ParentNode(Tags.p, text_to_children(no_end))),
            # "not code missing start": self.HTMLTestScenario(
            #     f"{no_start}",
            #     ParentNode(Tags.p, text_to_children(no_start))),
        }
        run_subtest_cases(self, block_to_html_node, test_cases)

    def test_quote_blocks(self):
        simple = "Don't worry, be happy"
        multiline = ("Line 1", "Line 2")
        empty = ""
        space = ""
        mixed = ("> Quote line", "Not quote")
        no_quote = "Not a quote"
        test_cases = {
            "simple quote": self.HTMLTestScenario(
                f"> {simple}",
                ParentNode(Tags.blockquote, text_to_children(simple))
            ),
            "multiline quote": self.HTMLTestScenario(
                "> {}\n> {}".format(*multiline),
                ParentNode(Tags.blockquote, text_to_children(' '.join(multiline)))
            ),
            "empty quote": self.HTMLTestScenario(
                f">{empty}",
                ParentNode(Tags.blockquote, text_to_children(empty))
            ),  # Test this edge case
            "quote with space": self.HTMLTestScenario(
                f"> {space}",
                ParentNode(Tags.blockquote, text_to_children(space))
            ),  # And this one
            "mixed invalid": self.HTMLTestScenario(
                '\n'.join(mixed),
                ParentNode(Tags.p, text_to_children(' '.join(mixed)))
            ),
            "missing gt": self.HTMLTestScenario(
                no_quote,
                ParentNode(Tags.p, text_to_children(no_quote))
            ),
        }
        run_subtest_cases(self, block_to_html_node, test_cases)

    def test_unordered_list_blocks(self):
        list_items_content = ["First item", "Second item with *italic*", "Third item"]

        no_space = "-Item"
        mixed = ("- Item 1", "Not a list item")
        missing_dashes = ("- Item 1", "- Item 2", "Plain text")
        text_start = ("Not a list", "- Item 1")
        test_cases = {
            "single item": self.HTMLTestScenario(
                f"{BlockType.UNORDERED_LIST} {list_items_content[0]}",
                ParentNode(
                    Tags.ul,  # The parent is an unordered list
                    [         # The children are a list of list items
                        ParentNode(Tags.li, text_to_children(list_items_content[0]))
                    ]
                ),
            ),
            "multiple items": self.HTMLTestScenario(
                '\n'.join(
                    f"{BlockType.UNORDERED_LIST} {item}" for item in list_items_content
                ),
                ParentNode(
                    Tags.ul,  # The parent is an unordered list
                    [         # The children are a list of list items
                        ParentNode(Tags.li, text_to_children(content))
                        for content in list_items_content
                    ]
                )
            ),
            "with spaces": self.HTMLTestScenario(
                f"-   {list_items_content[0]}",
                ParentNode(
                    Tags.ul,  # The parent is an unordered list
                    [         # The children are a list of list items
                        ParentNode(Tags.li, text_to_children(list_items_content[0]))
                    ]
                )
            ),
            "empty item": self.HTMLTestScenario(
                "- ",
                ParentNode(
                    Tags.ul,  # The parent is an unordered list
                    [         # The children are a list of list items
                        ParentNode(Tags.li, text_to_children(''))
                    ]
                )
            ),
            "no space after dash": self.HTMLTestScenario(
                no_space,
                ParentNode(Tags.p, text_to_children(no_space)),
            ),
            "mixed valid invalid": self.HTMLTestScenario(
                '\n'.join(mixed),
                ParentNode(Tags.p, text_to_children(' '.join(mixed))),
            ),
            "some lines missing dash": self.HTMLTestScenario(
                '\n'.join(missing_dashes),
                ParentNode(Tags.p, text_to_children(' '.join(missing_dashes))),
            ),
            "starts with text": self.HTMLTestScenario(
                '\n'.join(text_start),
                ParentNode(Tags.p, text_to_children(' '.join(text_start))),
            ),
        }        
        run_subtest_cases(self, block_to_html_node, test_cases)

    def test_ordered_lists(self):
        list_items_content = ("First item", "Second item with *bold*", "Third item")
        # multiline_item_content = ("Item 1\nLine 2", "Item 2") # Test a multiline list item

        zero_start = "0. Zero start"
        two_start = "2. Wrong start"
        skips_number = ("1. First", "3. Skipped two")
        wrong_sequence = ("1. First", "3. Wrong", "2. Wrong")
        no_space = "1.NoSpace"
        no_period = "1 No period"
        mixed = ("1. First", "Plain text")
        not_numbered = ("1. First", "2. Second", "- Not numbered")
        double_digits = ("1. First", "2. Second", "10. Jump to ten")
        test_cases = {
            "single item": self.HTMLTestScenario(
                f"1. {list_items_content[0]}",
                ParentNode(
                    Tags.ol,  # The parent is an ordered list
                    [         # The children are a list of list items
                        ParentNode(Tags.li, text_to_children(list_items_content[0])),  # First list item
                    ]
                )
            ),
            "multiple items": self.HTMLTestScenario(
                '\n'.join(
                    f"{idx}. {item}" for idx, item in enumerate(list_items_content, 1)
                ),
                ParentNode(
                    Tags.ol,  # The parent is an ordered list
                    [         # The children are a list of list items
                        ParentNode(Tags.li, text_to_children(content))
                        for content in list_items_content
                    ]
                )
            ),
            "with extra spaces": self.HTMLTestScenario(
                f"1.   {list_items_content[0]}",
                ParentNode(
                    Tags.ol,  # The parent is an ordered list
                    [         # The children are a list of list items
                        ParentNode(Tags.li, text_to_children(list_items_content[0])),             # First list item
                    ]
                )
            ),
           "empty item": self.HTMLTestScenario(
                "1. ",
                ParentNode(
                    Tags.ol,  # The parent is an ordered list
                    [         # The children are a list of list items
                        ParentNode(Tags.li, text_to_children("")),
                    ]
                )
            ),
            
            # Invalid cases - should be PARAGRAPH
            "starts with 0": self.HTMLTestScenario(
                zero_start,
                ParentNode(Tags.p, text_to_children(zero_start)),
            ),
            "starts with 2": self.HTMLTestScenario(
                two_start,
                ParentNode(Tags.p, text_to_children(two_start)),
            ),
            "skips number": self.HTMLTestScenario(
                '\n'.join(skips_number),
                ParentNode(Tags.p, text_to_children(' '.join(skips_number))),
            ),
            "wrong sequence": self.HTMLTestScenario(
                '\n'.join(wrong_sequence),
                ParentNode(Tags.p, text_to_children(' '.join(wrong_sequence))),
            ),
            "no space after period": self.HTMLTestScenario(
                no_space,
                ParentNode(Tags.p, text_to_children(no_space)),
            ),
            "no period": self.HTMLTestScenario(
                no_period,
                ParentNode(Tags.p, text_to_children(no_period)),
            ),
            "mixed with text": self.HTMLTestScenario(
                '\n'.join(mixed),
                ParentNode(Tags.p, text_to_children(' '.join(mixed))),
            ),
            "some lines not numbered": self.HTMLTestScenario(
                '\n'.join(not_numbered),
                ParentNode(Tags.p, text_to_children(' '.join(not_numbered))),
            ),
            "double digits": self.HTMLTestScenario(
                '\n'.join(double_digits),
                ParentNode(Tags.p, text_to_children(' '.join(double_digits))),
            ),
        }
        run_subtest_cases(self, block_to_html_node, test_cases)

    def test_paragraphs(self):
        simple = "Just some plain text"
        multiline = ("Line 1", "Line 2", "Line 3")
        markdown = "This has **bold** and *italic* text"
        num_sym = "Some text with 123 and @#$ symbols"
        special = "Text with ñ, é, ü, and 中文"
        punctuation = "Lots of punctuation!!! What? Yes... (maybe)"
        url_mail = "Visit https://example.com or email test@example.com"
        mixed_symbols = "$100 + 50% = good deal & more @ store"
        empty_string = ""
        whitespace = "   \t  "
        test_cases = {
            "simple text": self.HTMLTestScenario(simple, ParentNode(Tags.p, text_to_children(simple))),
            "multiline text": self.HTMLTestScenario(
                '\n'.join(multiline), ParentNode(Tags.p, text_to_children(' '.join(multiline)))),
            "text with markdown": self.HTMLTestScenario(markdown, ParentNode(Tags.p, text_to_children(markdown))),
            "numbers and symbols": self.HTMLTestScenario(num_sym, ParentNode(Tags.p, text_to_children(num_sym))),
            "special characters": self.HTMLTestScenario(special, ParentNode(Tags.p, text_to_children(special))),
            "punctuation heavy": self.HTMLTestScenario(punctuation, ParentNode(Tags.p, text_to_children(punctuation))),
            "urls and emails": self.HTMLTestScenario(url_mail, ParentNode(Tags.p, text_to_children(url_mail))),
            "mixed symbols": self.HTMLTestScenario(mixed_symbols, ParentNode(Tags.p, text_to_children(mixed_symbols))),
            "empty string": self.HTMLTestScenario(empty_string, ParentNode(Tags.p, text_to_children(empty_string))),
            "just whitespace": self.HTMLTestScenario(whitespace, ParentNode(Tags.p, text_to_children(whitespace))),  # If whitespace isn't stripped
        }
        run_subtest_cases(self, block_to_html_node, test_cases)


if __name__ == "__main__":
    unittest.main()