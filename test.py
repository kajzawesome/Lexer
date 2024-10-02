import os
import project4
import sys
import pytest
import time

TIME_CONSTRAINT = 150

@pytest.fixture
def bucket(request):
    return request.config.getoption("--bucket")

def read_file_contents(filepath):
    with open(filepath, "r") as f:
        return f.read()

def test_project1(bucket):
    TEST_ROOT_DIR = "./project4-passoff/" + bucket
    test_filenames = [f for f in os.listdir(TEST_ROOT_DIR) if f.startswith("input")]
    passed = True
    start_time = time.time()
    for filename in test_filenames:
        input_file = os.path.join(TEST_ROOT_DIR, filename)
        input_contents = read_file_contents(input_file)

        answer_file = os.path.join(TEST_ROOT_DIR, filename.replace('input', 'answer'))
        answer_contents = read_file_contents(answer_file)
        output = project4.project4(input_contents)
        try:
            assert answer_contents.rstrip() == output.rstrip()
            print("\n")
            print("Passed test: " + filename)
        except AssertionError as e:
            passed = False
            print("\n")
            print("Failed input: " + filename)
            print("-" * 100)
            assertion_error = str(e)
            assertion_error = assertion_error[assertion_error.find('\n  ') + 1:]
            print(assertion_error)
            print("-" * 100)
    ### TIME CONSTRAINT         
    elapsed_time = time.time() - start_time
    if elapsed_time > TIME_CONSTRAINT:
        passed = False
        print(f"You have exceeded the time limit of {TIME_CONSTRAINT} seconds.")
    print(f"This test took {elapsed_time} seconds to run.")
    assert passed

