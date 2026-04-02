import os
import sys
import argparse
import subprocess
import time

GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"

class tests:
    def __init__(self):
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.temp_dir = os.path.join(self.project_root, "temp")
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)
        os.makedirs(self.temp_dir)
        self.test_dir = os.path.join(self.project_root, "tests")

        self.available_tests = [
            test for test in os.listdir(self.test_dir)
            if test.endswith(".py") and not test.startswith("__")
        ]

    def _run_script(self, test_name):
        start_time = time.time()
        env = os.environ.copy()
        env["PYTHONPATH"] = self.project_root + ":" + env.get("PYTHONPATH", "")
        completed = subprocess.run(
            ["python3", f"{self.test_dir}/{test_name}"],
            env=env,
        )
        return completed.returncode, time.time() - start_time

    def _print_summary(self, exit_code, duration):
        status = f"{GREEN}Success{RESET}" if exit_code == 0 else f"{RED}Failed{RESET}"
        print(f"{status} (Exit code: {exit_code}) ({duration:.3f}s)")

    def run_test(self, test_name):
        if not test_name:
            global_exit_code = 0
            for test in self.available_tests:
                print(f"Executing test {test.split('.')[0]}", end=": ")
                exit_code, duration = self._run_script(test)
                self._print_summary(exit_code, duration)
                if exit_code != 0:
                    global_exit_code = 1
            return global_exit_code
            

        if test_name and not test_name.endswith(".py"):
            test_name += ".py"

        if test_name not in self.available_tests:
            print(f"Test '{test_name}' not found.")
            return 1

        print(f"Executing test {test_name.split('.')[0]}", end=": ")
        exit_code, duration = self._run_script(test_name)
        self._print_summary(exit_code, duration)
        return exit_code

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute the application tests.")
    parser.add_argument("--test", type=str, help="Name of the test to execute (e.g.: Strava_login)")
    args = parser.parse_args()

    test_runner = tests()
    exit_code = test_runner.run_test(args.test)
    sys.exit(exit_code)