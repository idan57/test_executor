import os

from test_executor.test_generation.test_executor import TestExecutor
from test_executor.test_generation.test_loader import TestLoader


def test_e2e_testing():
    tests_path = os.path.join(os.path.dirname(__file__), "mocked_tests")
    tests = TestLoader.load_tests(tests_path)
    executor = TestExecutor()

    executor.execute(tests)
