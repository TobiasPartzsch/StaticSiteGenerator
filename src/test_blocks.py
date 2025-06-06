import unittest

from blocks import BlockType, block_to_block_type
from testscenarios import StringConversionScenario, run_subtest_cases


BlockTestScenario = StringConversionScenario[BlockType]


class TestBlockToBlockType(unittest.TestCase):
    def test_headings(self):
        test_cases = {
            "h1": BlockTestScenario("# Heading 1", BlockType.HEADING),
            "h2": BlockTestScenario("## Heading 2", BlockType.HEADING),
            "h6": BlockTestScenario("###### Heading 6", BlockType.HEADING),
            "heading with extra text": BlockTestScenario("### Hello World!", BlockType.HEADING),
            "not heading no space": BlockTestScenario("#NoSpace", BlockType.PARAGRAPH),
            "not heading too many": BlockTestScenario("####### Too many hashes", BlockType.PARAGRAPH),
            "not heading zero": BlockTestScenario("Heading without hash", BlockType.PARAGRAPH),
        }
        run_subtest_cases(self, block_to_block_type, test_cases)

    def test_code_blocks(self):
        test_cases = {
            "simple code": BlockTestScenario("```\nprint('hello')\n```", BlockType.CODE),
            "multiline code": BlockTestScenario("```\nline1\nline2\nline3\n```", BlockType.CODE),
            "empty code": BlockTestScenario("```\n```", BlockType.CODE),
            "not code missing end": BlockTestScenario("```\ncode without end", BlockType.PARAGRAPH),
            "not code missing start": BlockTestScenario("code without start\n```", BlockType.PARAGRAPH),
        }
        run_subtest_cases(self, block_to_block_type, test_cases)

    def test_quote_blocks(self):
        test_cases = {
            "simple quote": BlockTestScenario("> Don't worry, be happy", BlockType.QUOTE),
            "multiline quote": BlockTestScenario("> Line 1\n> Line 2", BlockType.QUOTE),
            "empty quote": BlockTestScenario(">", BlockType.QUOTE),  # Test this edge case
            "quote with space": BlockTestScenario("> ", BlockType.QUOTE),  # And this one
            "mixed invalid": BlockTestScenario("> Quote line\nNot quote", BlockType.PARAGRAPH),
            "missing gt": BlockTestScenario("Not a quote", BlockType.PARAGRAPH),
        }
        run_subtest_cases(self, block_to_block_type, test_cases)

    def test_unordered_list_blocks(self):
        test_cases = {
            "single item": BlockTestScenario("- Item 1", BlockType.UNORDERED_LIST),
            "multiple items": BlockTestScenario("- Item 1\n- Item 2\n- Item 3", BlockType.UNORDERED_LIST),
            "with spaces": BlockTestScenario("-   Item with extra spaces", BlockType.UNORDERED_LIST),
            "empty item": BlockTestScenario("- ", BlockType.UNORDERED_LIST),
            "no space after dash": BlockTestScenario("-Item", BlockType.PARAGRAPH),
            "mixed valid invalid": BlockTestScenario("- Item 1\nNot a list item", BlockType.PARAGRAPH),
            "some lines missing dash": BlockTestScenario("- Item 1\n- Item 2\nPlain text", BlockType.PARAGRAPH),
            "starts with text": BlockTestScenario("Not a list\n- Item 1", BlockType.PARAGRAPH),
        }        
        run_subtest_cases(self, block_to_block_type, test_cases)

    def test_ordered_lists(self):
        test_cases = {
            "single item": BlockTestScenario("1. First item", BlockType.ORDERED_LIST),
            "multiple items": BlockTestScenario("1. First\n2. Second\n3. Third", BlockType.ORDERED_LIST),
            "with extra spaces": BlockTestScenario("1.   Item with spaces", BlockType.ORDERED_LIST),
            "empty item": BlockTestScenario("1. ", BlockType.ORDERED_LIST),
            
            # Invalid cases - should be PARAGRAPH
            "starts with 0": BlockTestScenario("0. Zero start", BlockType.PARAGRAPH),
            "starts with 2": BlockTestScenario("2. Wrong start", BlockType.PARAGRAPH),
            "skips number": BlockTestScenario("1. First\n3. Skipped two", BlockType.PARAGRAPH),
            "wrong sequence": BlockTestScenario("1. First\n2. Second\n4. Wrong", BlockType.PARAGRAPH),
            "no space after period": BlockTestScenario("1.NoSpace", BlockType.PARAGRAPH),
            "no period": BlockTestScenario("1 No period", BlockType.PARAGRAPH),
            "mixed with text": BlockTestScenario("1. First\nPlain text", BlockType.PARAGRAPH),
            "some lines not numbered": BlockTestScenario("1. First\n2. Second\n- Not numbered", BlockType.PARAGRAPH),
            "double digits": BlockTestScenario("1. First\n2. Second\n10. Jump to ten", BlockType.PARAGRAPH),
        }
        run_subtest_cases(self, block_to_block_type, test_cases)

    def test_paragraphs(self):
        test_cases = {
            "simple text": BlockTestScenario("Just some plain text", BlockType.PARAGRAPH),
            "multiline text": BlockTestScenario("Line 1\nLine 2\nLine 3", BlockType.PARAGRAPH),
            "text with markdown": BlockTestScenario("This has **bold** and *italic* text", BlockType.PARAGRAPH),
            "numbers and symbols": BlockTestScenario("Some text with 123 and @#$ symbols", BlockType.PARAGRAPH),
            "special characters": BlockTestScenario("Text with ñ, é, ü, and 中文", BlockType.PARAGRAPH),
            "punctuation heavy": BlockTestScenario("Lots of punctuation!!! What? Yes... (maybe)", BlockType.PARAGRAPH),
            "urls and emails": BlockTestScenario("Visit https://example.com or email test@example.com", BlockType.PARAGRAPH),
            "mixed symbols": BlockTestScenario("$100 + 50% = good deal & more @ store", BlockType.PARAGRAPH),
            "almost heading": BlockTestScenario("#but no space after", BlockType.PARAGRAPH),
            "almost list": BlockTestScenario("- but\nno dash on second line", BlockType.PARAGRAPH),
            "almost code": BlockTestScenario("```missing end", BlockType.PARAGRAPH),
            "empty string": BlockTestScenario("", BlockType.PARAGRAPH),
            "just whitespace": BlockTestScenario("   \t  ", BlockType.PARAGRAPH),  # If whitespace isn't stripped
        }
        run_subtest_cases(self, block_to_block_type, test_cases)

if __name__ == "__main__":
    unittest.main()