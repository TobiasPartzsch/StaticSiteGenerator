from typing import Callable, NamedTuple
from unittest import TestCase

class TestScenario(NamedTuple):
    input: str
    expected: list[str]


def run_subtest_cases(
    test_instance: TestCase,
    test_function: Callable[[str], list[str]],
    test_cases: dict[str, TestScenario]
) -> None:
    """Helper to run multiple test cases as subtests"""
    for case_name, case_data in test_cases.items():
        with test_instance.subTest(case=case_name):
            result = test_function(case_data.input)
            test_instance.assertEqual(result, case_data.expected)
