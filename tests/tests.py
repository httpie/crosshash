import json
import random
import subprocess
from functools import partial
from itertools import combinations
from pathlib import Path
from pprint import pprint

import pytest

from . import gen
# noinspection PyProtectedMember
from crosshash import MAX_SAFE_INTEGER, ERROR_UNSAFE_NUMBER


HERE = Path(__file__).parent
ROOT = HERE.parent

IMPLEMENTATIONS = {
    'Python': ('python3', ROOT / 'crosshash.py'),
    'JavaScript': ('node', HERE / 'main.js'),
}
NUM_CASES = 100
MAX_DEPTH = 10
MAX_HEIGHT = 10
MAX_STR_LEN = 10
GENERATORS = [
    partial(gen.random_string, max_len=MAX_STR_LEN),
    partial(gen.random_int, max_val=MAX_SAFE_INTEGER),
    gen.random_bool,
    partial(gen.random_float, max_size=MAX_SAFE_INTEGER),
]
GENERATORS = [
    *GENERATORS,
    partial(gen.random_list, GENERATORS),
]

CASES_OK = [
    {'float_with_no_fraction': 1.0},
    {'emojis': '🚀👨‍⚖️👩🏼‍🔬'},
    {'non_latin': 'čćžšđ'},
    {'null_character': '\0'},
]

CASES_UNSAFE_NUMBERS = [
    {'unsafe_int': MAX_SAFE_INTEGER + 1},
    {'unsafe_float': MAX_SAFE_INTEGER + 1.1},
]


def cases(max_depth=MAX_DEPTH, max_height=MAX_HEIGHT, num_cases=NUM_CASES):
    # noinspection PyTypeChecker
    yield from CASES_OK
    # noinspection PyTypeChecker
    yield from (
        gen.random_dict(
            max_depth=random.randint(1, max_depth),
            max_height=random.randint(1, max_height),
            generators=GENERATORS
        )
        for _ in range(num_cases)
    )


@pytest.mark.parametrize('data', CASES_UNSAFE_NUMBERS)
def test_unsafe_numbers(data):
    assert_all_fail(
        data=data,
        output_format='--json',
        error_message=ERROR_UNSAFE_NUMBER,
    )


@pytest.mark.parametrize('data', cases())
def test_json(data: dict):
    assert_all_equal(data=data, output_format='--json')


@pytest.mark.parametrize('data', cases())
def test_hash(data: dict):
    assert_all_equal(data=data, output_format='--hash')


def assert_all_equal(data: dict, output_format: str):
    """
    Assert that all implementations return the same output.

    Each implementation is called with a different randomized key order.

    """
    outputs = {
        name: get_output(shuffle_keys(data), cmd, output_format)
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


def assert_all_fail(data: dict, output_format: str, error_message: str):
    for name, cmd in IMPLEMENTATIONS.items():
        print()
        print(name)
        output = get_output(data=data, cmd=cmd, output_format=output_format, expect_success=False)
        print(output)
        assert error_message in output
        print()


def get_output(data: dict, cmd: tuple, output_format: str, expect_success=True):
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
