import json
import random
import subprocess
from itertools import combinations
from pathlib import Path
from pprint import pprint

from crosshash import JSON


ROOT = Path(__file__).parent.parent.absolute()


class Implementation:
    def __init__(self, executable: Path):
        self.executable = executable

    def __str__(self):
        return self.executable.name

    def get_output(self, data: JSON, output_format='--hash', expect_success=True):
        input_json = json.dumps(data)
        return self.run(output_format, input_json, expect_success=expect_success)

    def get_hash(self, data: JSON, expect_success=True):
        return self.get_output(data=data, output_format='--hash', expect_success=expect_success)

    def get_json(self, data: JSON, expect_success=True):
        return self.get_output(data=data, output_format='--json', expect_success=expect_success)

    def run(self, *args, expect_success=True):
        return get_command_output(cmd=[self.executable, *args], expect_success=expect_success)


IMPLEMENTATIONS: list[Implementation] = [
    Implementation(ROOT / 'crosshash.py'),
    Implementation(ROOT / 'crosshash.js'),
]


def get_command_output(*, cmd: list[str], expect_success=True):
    print(cmd)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, _ = process.communicate()
    output = output.decode().strip()
    if expect_success:
        if process.returncode:
            raise Exception(output)
    else:
        assert process.returncode
    return output


def assert_all_equal(data: JSON, output_format: str):
    """
    Assert that all implementations return the same output.

    Each implementation is called with a different randomized key order.

    """
    outputs = {
        imp: imp.get_output(data=shuffle_keys(data), output_format=output_format) for imp in IMPLEMENTATIONS
    }
    assert len(set(outputs.values())) == 1, outputs


def assert_all_fail(data: JSON, output_format: str, error_message: str):
    for imp in IMPLEMENTATIONS:
        print()
        print(imp)
        output = imp.get_output(data=data, output_format=output_format, expect_success=False)
        print(output)
        assert error_message in output
        print()


def shuffle_keys(val):
    if isinstance(val, dict):
        keys = list(val.keys())
        random.shuffle(keys)
        val = {k: shuffle_keys(val[k]) for k in keys}
    elif isinstance(val, list):
        val = [shuffle_keys(v) for v in val]
    return val
