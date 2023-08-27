"""
Stable JSON serialization and hashing for Python and JavaScript.

<https://github.com/httpie/crosshash>

"""
import hashlib
import json

__all__ = ['crossjson', 'crosshash', 'CrossHashError', 'MAX_SAFE_INTEGER']

# <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_SAFE_INTEGER>
MAX_SAFE_INTEGER = 9007199254740991  # 2**53 - 1
ERROR_UNSAFE_NUMBER = 'ERROR_UNSAFE_NUMBER'


class CrossHashError(ValueError):
    pass


def crossjson(obj: dict) -> str:
    obj = clean(obj)
    return json.dumps(
        obj=obj,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
        separators=(',', ':'),
    )


def crosshash(obj: dict) -> str:
    return hash_string(crossjson(obj))


def hash_string(s: str) -> str:
    return hashlib.md5(s.encode()).hexdigest()


def clean(value):
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


if __name__ == '__main__':
    import sys


    def main(action, input_json):
        do_hash = {'--json': False, '--hash': True}[action]
        output = crossjson(json.loads(input_json))
        if do_hash:
            output = hash_string(output)
        return output


    try:
        input_json = sys.argv[2]
    except IndexError:
        input_json = json.dumps({"a": 1.0})
    print(main(action=sys.argv[1], input_json=input_json))
