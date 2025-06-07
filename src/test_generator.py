import unittest

from generator import extract_title
from testscenarios import ErrorRaisingScenario, StringConversionScenario, run_subtest_cases_equal, run_subtest_cases_error


class TestBlockToBlockType(unittest.TestCase):
    TitleTestScenario = StringConversionScenario[str]
    ValueErrorScenario = ErrorRaisingScenario

    def test_extract_title(self):
        titles = (
            "Title Heading 1",  # simple_title
            "C# Programming Language",  # title itself contains the # character
            "Lots of spaces ",  # titles with extra spaces
            "# ## Double Trouble",  # multiple # characters that aren't meant to be stripped
            "#  Title with leading space",  # title that starts with a space
        )

        test_cases = {
            title: self.TitleTestScenario(
                input=f"# {title}",
                expected=title
            )
            for title in titles
        }
        run_subtest_cases_equal(self, extract_title, test_cases)

        markups = (
            '',  # empty
            ' ',  # space
            '   \t   ',  # whitespace
            "text\nsome more\nnot finished yet.",  # no_headers
            "## Second Level\n### Third Level",  # headers, but they're all h2 or lower
            "some people think C# is cool",  # # in the middle of text
            "#this is actually no header",  # # at start but no space
        )
        msg_format = "No first-level heading found in {markup}"

        test_cases = {
            markup: self.ValueErrorScenario(
                input=markup,
                expected_err=ValueError,
                expected_msg=msg_format.format(markup=markup)
            )
            for markup in markups
        }
        run_subtest_cases_error(self, extract_title, test_cases)
