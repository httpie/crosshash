import random
from functools import partial
from typing import Iterable

from crosshash import MAX_SAFE_INTEGER, JSON
from tests import gen


# Configuration of generated test cases
GEN_NUM_CASES = 100
GEN_DICT_MAX_DEPTH = 10
GEN_MAX_HEIGHT = 10
GEN_MAX_STR_LEN = 10
GEN_MAX_NUMBER = MAX_SAFE_INTEGER
GENERATORS = (
    partial(gen.random_string, max_len=GEN_MAX_STR_LEN),
    partial(gen.random_int, max_val=GEN_MAX_NUMBER),
    gen.random_bool,
    partial(gen.random_float, max_size=GEN_MAX_NUMBER),
)
GENERATORS = (
    *GENERATORS,
    partial(gen.random_list, GENERATORS),
)


# Manual test cases that should be cross-hashable
CASES_OK: list[JSON] = [
    0,
    0.1,
    1,
    1.0,
    1.1,
    '',
    '\0',
    'AAA',
    'بايثون',
    'ジャバスクリプト',
    '🚀👨‍⚖️👩🏼‍🔬',
    True,
    False,
    None,
    [1, 2, 3, 'AAA', 'BBB', 'CCC'],
    [],
    {},
    {'empty': ''},
    {'float_with_fraction': 1.1},
    {'float_with_no_fraction': 1.0},
    {'emojis': '🚀👨‍⚖️👩🏼‍🔬'},
    {'non_latin': 'čćžšđ'},
    {'null_character': '\0'},
]


# Manual test cases that shouldn’t be cross-hashable due to unsafe numbers
CASES_UNSAFE_NUMBERS: list[JSON] = [
    {'unsafe_int': MAX_SAFE_INTEGER + 1},
    {'unsafe_float': MAX_SAFE_INTEGER + 1.1},
]


def generate_cases(
        max_depth=GEN_DICT_MAX_DEPTH,
        max_height=GEN_MAX_HEIGHT,
        num_cases=GEN_NUM_CASES,
        generators=GENERATORS,
) -> Iterable[dict[str, JSON]]:
    return (
        gen.random_dict(
            max_depth=random.randint(1, max_depth),
            max_height=random.randint(1, max_height),
            generators=generators,
        )
        for _ in range(num_cases)
    )
