#!/usr/bin/env python3
"""
`crosshash` — stable JSON serialization and hashing for Python and JavaScript

<https://github.com/httpie/crosshash>


CLI usage:
    python3 -m crosshash --json '{"foo": "bar"}'
    python3 -m crosshash --hash '{"foo": "bar"}'

"""
import hashlib
import json
from textwrap import dedent
from typing import TypeAlias


__all__ = ('crossjson', 'crosshash', 'CrossHashError', 'MAX_SAFE_INTEGER', 'JSON', 'ERROR_UNSAFE_NUMBER')

# <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_SAFE_INTEGER>
MAX_SAFE_INTEGER = 9007199254740991  # 2**53 - 1

# For tests
ERROR_UNSAFE_NUMBER = 'ERROR_UNSAFE_NUMBER'

# <https://github.com/python/typing/issues/182#issuecomment-1320974824>
JSON: TypeAlias = dict[str, 'JSON'] | list['JSON'] | str | int | float | bool | None


class CrossHashError(ValueError):
    pass


def crossjson(obj: JSON) -> str:
    obj = clean(obj)
    return json.dumps(
        obj=obj,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
        separators=(',', ':'),
    )


def crosshash(obj: JSON) -> str:
    return md5(crossjson(obj))


def md5(s: str) -> str:
    return hashlib.md5(s.encode()).hexdigest()


def clean(value: JSON) -> JSON:
    if isinstance(value, int):
        validate_number(value)
    elif isinstance(value, float):
        validate_number(value)
        value = clean_float(value)
    elif isinstance(value, dict):
        value = {k: clean(v) for k, v in value.items()}
    elif isinstance(value, list):
        value = [clean(item) for item in value]
    return value


def is_safe_number(value: int | float) -> bool:
    """
    Return True if value can be hashed safely across JS/Python.

    """
    return -MAX_SAFE_INTEGER <= value <= MAX_SAFE_INTEGER


def validate_number(value: int | float):
    if not is_safe_number(value):
        raise CrossHashError(f'{ERROR_UNSAFE_NUMBER}: {value}')


def clean_float(value: float):
    """
    Apply same formatting to float as JS does.

    >>> clean_float(1.0)
    1
    """
    as_int = int(value)
    if value == as_int:
        value = as_int
    return value


def main():
    import sys
    if len(sys.argv) != 3 or sys.argv[1] not in ('--json', '--hash'):
        print(__doc__)
        sys.exit(1)
    action, input_json = sys.argv[1:]
    operation = {'--json': crossjson, '--hash': crosshash}[action]
    output = operation(json.loads(input_json))
    print(output)


if __name__ == '__main__':
    main()
