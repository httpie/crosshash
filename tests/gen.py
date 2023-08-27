"""
Adapted from: <https://github.com/LucaCappelletti94/random_dict>

<https://github.com/LucaCappelletti94/random_dict/blob/master/LICENSE>

MIT License

Copyright (c) 2019 Luca Cappelletti

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
import typing
from itertools import product
from random import randint, uniform, getrandbits, choice, shuffle
from string import digits, ascii_letters
from typing import Callable, List, Tuple, Dict


def random_string(max_len=1000):
    return ''.join(
        choice(ascii_letters + digits)
        for _ in range(randint(0, max_len))
    )


def random_int(max_val=1_000_000):
    return randint(1, max_val)


def random_list(generators, max_len=20) -> []:
    """Return a random tuple."""
    return [choice(generators)() for _ in range(randint(0, max_len))]


def random_float(max_size=1_000_000) -> float:
    """Return a random float."""
    return uniform(-max_size, max_size)


def random_bool() -> bool:
    """Return a random boolean."""
    return bool(getrandbits(1))


def random_bytes() -> bytes:
    """Return a random bytes sequence."""
    return random_string().encode()


def random_tuple() -> tuple:
    """Return a random tuple."""
    generators = random_int, random_float, random_bool, random_string, random_bytes
    first = choice(generators)
    second = choice(generators)
    return first(), second()


def _value_gen(sources: List[Callable], number: int) -> Callable:
    for _ in range(number):
        yield choice(sources)


def random_string_dict(max_depth: int, max_height: int) -> Dict:
    """Return a random dictionary of string with at most given max_depth and max_height.
        max_depth:int, maximum depth of dictionary.
        max_height:int, maximum height of dictionary.
    """
    return random_dict(max_depth, max_height, (random_string,))


def random_bool_dict(max_depth: int, max_height: int) -> Dict:
    """Return a random dictionary of bool with at most given max_depth and max_height.
        max_depth:int, maximum depth of dictionary.
        max_height:int, maximum height of dictionary.
    """
    return random_dict(max_depth, max_height, (random_bool,))


def random_float_dict(max_depth: int, max_height: int) -> Dict:
    """Return a random dictionary of floats with at most given max_depth and max_height.
        max_depth:int, maximum depth of dictionary.
        max_height:int, maximum height of dictionary.
    """
    return random_dict(max_depth, max_height, (random_float,))


def random_int_dict(max_depth: int, max_height: int) -> Dict:
    """Return a random dictionary of integers with at most given max_depth and max_height.
        max_depth:int, maximum depth of dictionary.
        max_height:int, maximum height of dictionary.
    """
    return random_dict(max_depth, max_height, (random_int,))


def random_dict(
        max_depth: int,
        max_height: int,
        generators: Tuple[Callable] = (
        random_int, random_bool, random_float, random_string, random_tuple, random_bytes),
        generators_combinations: int = 5
) -> Dict:
    """Return a random dictionary with at most given max_depth and max_height.

    Parameters
    ---------------------
        max_depth:int, maximum depth of dictionary.
        max_height:int, maximum height of dictionary.
        generators:Tuple[Callable], functions used to populate the dictionary.
        generators_combinations: int = 5, functions combinations to use.

    Returns
    ---------------------
    Random dictionary.
    """
    generators_tuples = list(product(_value_gen(
        generators, max_height), _value_gen(generators, max_height)))
    shuffle(generators_tuples)
    return {
        key_gen(): random_dict(randint(1, max_depth - 1), randint(1, max_height - 1),
                               generators) if max_depth > 1 and max_height > 1 else val_gen()
        for key_gen, val_gen in generators_tuples[:generators_combinations]
        if isinstance(key_gen(), typing.Hashable)
    }
