from dataclasses import dataclass
from typing import Callable, Generic, Mapping, TypeVar
from unittest import TestCase


T = TypeVar('T')

@dataclass(frozen=True)
class StringConversionScenario(Generic[T]):
    input: str
    expected: T


def run_subtest_cases(
    test_instance: TestCase,
    test_function: Callable[[str], T],
    test_cases: Mapping[str, StringConversionScenario[T]]
) -> None:
    """Generic helper to run multiple test cases as subtests"""
    for case_name, case_data in test_cases.items():
        with test_instance.subTest(case=case_name):
            result = test_function(case_data.input)
            test_instance.assertEqual(result, case_data.expected)