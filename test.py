import os
import sys
import argparse
import subprocess
import time
import shutil

GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"

class tests:
    def __init__(self):
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.temp_dir = os.path.join(self.project_root, "temp")
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        os.makedirs(self.temp_dir, exist_ok=True)
        self.test_dir = os.path.join(self.project_root, "tests")

        self.available_tests = []
        for file in os.listdir(self.test_dir):
            if file.endswith(".py") and not file.startswith("__"):
                try:
                    with open(os.path.join(self.test_dir, file), "r") as f:
                        content = f.read()
                        order_line = next((line for line in content.splitlines() if line.startswith("TEST_ORDER")), None)
                        if order_line:
                            order = int(order_line.split("=")[1].strip())
                            self.available_tests.append((order, file))
                        else:
                            self.available_tests.append((float('inf'), file))
                except Exception as e:
                    print(f"Error reading test file {file}: {e}")
                    self.available_tests.append((float('inf'), file))

        self.ordered_tests = sorted(self.available_tests, key=lambda x: x[0])

    def _run_script(self, test_name):
        start_time = time.time()
        env = os.environ.copy()
        existing_pythonpath = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = (self.project_root if not existing_pythonpath else self.project_root + os.pathsep + existing_pythonpath)
        completed = subprocess.run(
              [sys.executable, f"{self.test_dir}/{test_name}"],
            env=env,
        )
        return completed.returncode, time.time() - start_time

    def _print_summary(self, exit_code, duration):
        status = f"{GREEN}Success{RESET}" if exit_code == 0 else f"{RED}Failed{RESET}"
        print(f"{status} (Exit code: {exit_code}) ({duration:.3f}s)")

    def run_test(self, test_name):
        if not test_name:
            global_exit_code = 0
            for test in self.ordered_tests:
                if test[0] < 0:
                    print(f"Skipping test {test[1].split('.')[0]}")
                    continue
                print(f"Executing test {test[1].split('.')[0]}", end=": ")
                exit_code, duration = self._run_script(test[1])
                self._print_summary(exit_code, duration)
                if exit_code != 0:
                    global_exit_code = 1
            return global_exit_code
            

        if test_name and not test_name.endswith(".py"):
            test_name += ".py"

        if test_name not in [test[1] for test in self.available_tests]:
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