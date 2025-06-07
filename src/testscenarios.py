from dataclasses import dataclass
from typing import Callable, Generic, Mapping, TypeVar
from unittest import TestCase

# Define the type variable T just before the function or inside it if possible
# (though defining it before is more common for function-level generics)
T = TypeVar('T')

@dataclass(frozen=True)
class StringConversionScenario(Generic[T]):
    input: str
    expected: T

@dataclass(frozen=True)
class ErrorRaisingScenario:
    input: str
    expected_err: type[Exception]
    expected_msg: str


def run_subtest_cases_equal(
    test_instance: TestCase,
    test_function: Callable[[str], T],
    test_cases: Mapping[str, StringConversionScenario[T]]
) -> None:
    """Generic helper to run multiple test cases as subtests"""
    for case_name, case_data in test_cases.items():
        with test_instance.subTest(case=case_name):
            result = test_function(case_data.input)
            test_instance.assertEqual(result, case_data.expected)

def run_subtest_cases_error(
    test_instance: TestCase,
    test_function: Callable[[str], T],
    test_cases: Mapping[str, ErrorRaisingScenario]
) -> None:
    """Generic helper to run multiple test cases as subtests"""
    for case_name, case_data in test_cases.items():
        with test_instance.subTest(case=case_name):
            with test_instance.assertRaises(case_data.expected_err) as cm:
                test_function(case_data.input)
            test_instance.assertEqual(str(cm.exception), case_data.expected_msg)
