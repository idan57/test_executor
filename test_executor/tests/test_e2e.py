import os
import sys

main_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(main_folder)


if __name__ == '__main__':
    from test_generation.test_executor import TestExecutor
    from test_generation.test_loader import TestLoader

    tests_path = os.path.join(os.path.dirname(__file__), "mocked_tests")
    tests = TestLoader.load_tests(tests_path)
    executor = TestExecutor()

    executor.Logger.info("*" * 16 + " Start Execution " + "*" * 16)
    executor.execute(tests)
    executor.Logger.info("*" * 16 + " End Execution " + "*" * 16)
