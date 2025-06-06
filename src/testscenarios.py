from typing import Callable, NamedTuple, TypeVar
from unittest import TestCase

from blocks import BlockType

T = TypeVar('T')


class TextSplittingScenario(NamedTuple):
    input: str
    expected: list[str]

class BlockToBlockTypeScenario(NamedTuple):
    input: str
    expected: BlockType


def run_subtest_cases(
    test_instance: TestCase,
    test_function: Callable[[str], T],
    test_cases: dict[str, tuple[str, T]]
) -> None:
    """Generic helper to run multiple test cases as subtests"""
    for case_name, (input_data, expected) in test_cases.items():
        with test_instance.subTest(case=case_name):
            result = test_function(input_data)
            test_instance.assertEqual(result, expected)