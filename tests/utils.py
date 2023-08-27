import json
import random
import subprocess
from itertools import combinations
from pathlib import Path
from pprint import pprint

from crosshash import JSON


ROOT = Path(__file__).parent.parent


IMPLEMENTATIONS = {
    'Python': ('python3', ROOT / 'crosshash.py'),
    'JavaScript': ('node', ROOT / 'crosshash.js'),
}


def assert_all_equal(data: JSON, output_format: str):
    """
    Assert that all implementations return the same output.

    Each implementation is called with a different randomized key order.

    """
    outputs = {
        name: get_output(data=shuffle_keys(data), cmd=cmd, output_format=output_format)
        for name, cmd in IMPLEMENTATIONS.items()
    }
    if len(set(outputs.values())) > 1:
        for name_a, name_b in combinations(IMPLEMENTATIONS.keys(), 2):
            output_a, output_b = outputs[name_a], outputs[name_b]
            print(name_a)
            pprint(output_a)
            print(name_b)
            pprint(output_b)
            assert output_a == output_b


def assert_all_fail(data: JSON, output_format: str, error_message: str):
    for name, cmd in IMPLEMENTATIONS.items():
        print()
        print(name)
        output = get_output(data=data, cmd=cmd, output_format=output_format, expect_success=False)
        print(output)
        assert error_message in output
        print()


def get_output(data: JSON, cmd: tuple, output_format: str, expect_success=True):
    input_json = json.dumps(data)
    cmd = [*cmd, output_format, input_json]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, _ = process.communicate()
    output = output.decode().strip()
    if expect_success:
        if process.returncode:
            raise Exception(output)
    else:
        assert process.returncode
    return output


def shuffle_keys(val):
    if isinstance(val, dict):
        keys = list(val.keys())
        random.shuffle(keys)
        val = {k: shuffle_keys(val[k]) for k in keys}
    elif isinstance(val, list):
        val = [shuffle_keys(v) for v in val]
    return val
