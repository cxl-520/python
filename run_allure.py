# run_allure.py 跑全部的测试用例
import argparse
import os
import shutil

import pytest

ALLURE_TITLE = "Allure Report"

# Default target: run all tests under testcase
TEST_TARGET = ["testcase"]

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.environ.get("WORKSPACE")
BASE_DIR = WORKSPACE_DIR if WORKSPACE_DIR else ROOT_DIR
RESULT_DIR = os.path.join(BASE_DIR, "allure-results")
REPORT_DIR = os.path.join(BASE_DIR, "report")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("targets", nargs="*", help="test targets: file or directory")
    parser.add_argument("-k", dest="keyword", help="keyword expression")
    parser.add_argument("--report-name", default=ALLURE_TITLE, help="Allure report name")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.targets:
        test_target = args.targets
    elif args.keyword:
        test_target = ["-k", args.keyword]
    else:
        test_target = TEST_TARGET

    if os.path.exists(RESULT_DIR):
        shutil.rmtree(RESULT_DIR)
        print(f"cleaned: {RESULT_DIR}")

    if os.path.exists(REPORT_DIR):
        history_src = os.path.join(REPORT_DIR, "history")
        history_dst = os.path.join(RESULT_DIR, "history")
        if os.path.exists(history_src):
            os.makedirs(RESULT_DIR, exist_ok=True)
            shutil.copytree(history_src, history_dst)
            print("history copied")
        shutil.rmtree(REPORT_DIR)
        print(f"cleaned: {REPORT_DIR}")

    pytest_args = [
        *test_target,
        "-v",
        "-s",
        f"--alluredir={RESULT_DIR}",
    ]

    print(f"running: {pytest_args}")
    exit_code = pytest.main(pytest_args)

    print("generating report...")
    os.system(f'allure generate "{RESULT_DIR}" -o "{REPORT_DIR}" --clean --report-name "{args.report_name}"')
    os.system(f'allure open "{REPORT_DIR}"')

    if exit_code != 0:
        raise SystemExit(exit_code)
