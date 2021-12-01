import os
from typing import List

from test_executor.abstract_test.test_result import TestVerdict, TestResult
from test_executor.test_generation.test_executor import TestExecutor
from test_executor.test_generation.test_loader import TestLoader

tests_path = os.path.join(os.path.dirname(__file__), "mocked_tests")


class ListenerMock(object):
    """
    Mock for a listener
    """

    def __init__(self):
        self.results = []

    def notify(self, result: TestResult):
        self.results.append(result)


def execute(test_paths: List[str], concurrency: int = 1, listener=None, set_params=False, get_runnables=False):
    """
    Main execution flow

    :param get_runnables: True if should return runnables
    :param concurrency: concurrency level for executing
    :param test_paths: list of test paths
    :param listener: listener for the tests
    :param set_params: True if should set params in execution
    :return: results of the tests
    """
    loaded_tests = TestLoader.load_tests(test_paths)

    params = {}

    if set_params:
        params = {
            "MockTest1": {"1key1": "1", "1key2": "2"},
            "MockTest2": {"2key1": "1", "2key2": "2"},
            "MockTest1.test1": {"1key3": "1", "1key4": "2"},
        }

    test_executor = TestExecutor(concurrency_level=concurrency)

    test_executor.Logger.info("*" * 32 + " Start Execution " + "*" * 32)
    results = test_executor.execute(loaded_tests, listener=listener, custom_params=params)
    test_executor.Logger.info("*" * 32 + " End Execution " + "*" * 32)
    for result in results:
        assert result.verdict == TestVerdict.PASSED, f"Expected test {result.test_name} to pass"

    if get_runnables:
        return results, loaded_tests

    return results


def test_regular_flow():
    """
    Test regular features
    """
    execute([tests_path])


def test_regular_flow_set_params():
    """
    Test regular features with setting params
    """
    results, runnables = execute([tests_path], set_params=True, get_runnables=True)

    assert len(results) == len(runnables), "Expected runnables and results to have the same length"
    for runnable in runnables:
        if str(runnable).startswith("MockTest1") or str(runnable).startswith("MockTest2"):
            assert runnable._test_class.params, "Expected to have params"


def test_regular_flow_multiple_paths():
    """
    Tests multiple paths feature
    """
    results = execute([tests_path] * 3)

    assert len(results) == 18, f"Excepted to have 18 results but had: {len(results)}"


def test_regular_flow_parallel():
    """
    Test parallel execution feature
    """
    results = execute([tests_path] * 3, 18)

    assert len(results) == 18, f"Excepted to have 18 results but had: {len(results)}"


def test_regular_flow_parallel_and_listener():
    """
    Test parallel execution feature with listener
    """
    listener = ListenerMock()
    results = execute([tests_path] * 3, 18, listener=listener)

    assert len(results) == 18, f"Excepted to have 18 results but had: {len(results)}"
    assert results == listener.results, "Expected listener to have same results"


tests = [
    test_regular_flow,
    test_regular_flow_set_params,
    test_regular_flow_multiple_paths,
    test_regular_flow_parallel,
    test_regular_flow_parallel_and_listener
]

if __name__ == '__main__':
    import traceback

    executor = TestExecutor()
    failed = False

    for test in tests:
        try:
            executor.Logger.info("*" * 32)
            executor.Logger.info(f"Running: {test}")
            test()
            executor.Logger.info("Execution Ended")
            executor.Logger.info("*" * 32)
        except Exception as e:
            executor.Logger.error("An exception has occurred, traceback is below")
            executor.Logger.error(traceback.format_exc())
            failed = True

    if failed:
        raise Exception("Execution has ended with failures, please see them above")
