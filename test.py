import os
import argparse
import subprocess
import shutil
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

        self.available_tests = os.listdir(self.test_dir)
        for test in self.available_tests:
            if test.startswith("__") or not test.endswith(".py"):
                self.available_tests.remove(test)

    def _run_script(self, test_name):
        start_time = time.time()
        env = os.environ.copy()
        env["PYTHONPATH"] = self.project_root + ":" + env.get("PYTHONPATH", "")
        
        completed = subprocess.run(
            ["python3", f"{self.test_dir}/{test_name}"],
            capture_output=True,
            text=True,
            env=env,
        )
        return {
            "exit_code": completed.returncode,
            "success": completed.returncode == 0,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "execution_time": time.time() - start_time
        }

    def run_test(self, test_name):
        if not test_name:
            for test in self.available_tests:
                print(f"Executing test {test}", end=": ")
                result = self._run_script(test)
                self.print_results(result)
            return
            

        if test_name and not test_name.endswith(".py"):
            test_name += ".py"

        if test_name not in self.available_tests:
            print(f"Test '{test_name}' not found.")
            return

        print(f"Executing test {test_name}", end=": ")
        result = self._run_script(test_name)
        self.print_results(result)

    def print_results(self, result):
        execution_time = f"{result['execution_time']:.3f}s -"
        status = f"{GREEN}Success{RESET}" if result['success'] else f"{RED}Failed{RESET}"
        exit_code = f"(Exit code: {result['exit_code']})"
        stdout = f"stdout: {result['stdout']}" if result['stdout'] else ""
        stderr = f"stderr: {result['stderr']}" if result['stderr'] else ""


        print(f"{execution_time} {status} {exit_code} {stdout} {stderr}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute the application tests.")
    parser.add_argument("--test", type=str, help="Name of the test to execute (e.g.: Strava_login)")
    args = parser.parse_args()

    test_runner = tests()
    test_results = test_runner.run_test(args.test)