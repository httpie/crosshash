import json
import random
import subprocess
from itertools import combinations
from pathlib import Path
from pprint import pprint

from crosshash import JSON


ROOT = Path(__file__).parent.parent.absolute()


IMPLEMENTATIONS: list[Path] = [
    ROOT / 'crosshash.py',
    ROOT / 'crosshash.js',
]


def assert_all_equal(data: JSON, output_format: str):
    """
    Assert that all implementations return the same output.

    Each implementation is called with a different randomized key order.

    """
    outputs = {
        exe: get_output(data=shuffle_keys(data), exe=exe, output_format=output_format)
        for exe in IMPLEMENTATIONS
    }
    if len(set(outputs.values())) > 1:
        for exe_a, exe_b in combinations(IMPLEMENTATIONS, 2):
            output_a, output_b = outputs[exe_a], outputs[exe_b]
            print(exe_a.name)
            pprint(output_a)
            print(exe_b.name)
            pprint(output_b)
            assert output_a == output_b


def assert_all_fail(data: JSON, output_format: str, error_message: str):
    for exe in IMPLEMENTATIONS:
        print()
        print(exe.name)
        output = get_output(data=data, exe=exe, output_format=output_format, expect_success=False)
        print(output)
        assert error_message in output
        print()


def get_output(*, exe: Path, output_format: str, data: JSON, expect_success=True):
    input_json = json.dumps(data)
    cmd = [str(exe), output_format, input_json]
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
