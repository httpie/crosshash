# `crosshash`

[![Build status](https://github.com/httpie/crosshash/workflows/test/badge.svg)](https://github.com/httpie/crosshash/actions)

Stable, cross-platform JSON serialization and hashing for Python and JavaScript.

## Why?

To make it possible to compare and hash JSON objects in a stable way across platforms.

## How?

- Sort keys alphabetically
- Ensure no unsafe numbers are present 
- Use the same format as `JSON.stringify()` (lowest common denominator) 
- Hash the resulting string with MD5

## Installation


### Python

https://pypi.org/project/crosshash

```bash
pip install crosshash
```

### JavaScript

https://www.npmjs.com/package/crosshash

```bash
npm install crosshash
```

## Usage

### Python

```python
from crosshash import crossjson, crosshash, CrossHashError, MAX_SAFE_INTEGER

obj = {
    'B': 2,
    'C': [1, 2, 3],
    'A': 1,
}
assert crossjson(obj) == '{"A":1,"B":2,"C":[1,2,3]}'  # stable JSON
assert crosshash(obj) == '12982c60a9a8829ea4eeb2e1e7e1e04e'  # stable hash

crosshash({'A': MAX_SAFE_INTEGER + 1})  # throws CrossHashError

```

### JavaScript

```javascript
const {crossjson, crosshash, CrossHashError} = require('crosshash')

const obj = {
    B: 2,
    C: [1, 2, 3],
    A: 1,
}
assert(crossjson(obj) === '{"A":1,"B":2,"C":[1,2,3]}') // stable JSON
assert(crosshash(obj) === '12982c60a9a8829ea4eeb2e1e7e1e04e') // stable hash

crosshash({a: Number.MAX_SAFE_INTEGER + 1}) // throws CrossHashError

```


## Test suite

To ensure consistency, the [test suite](tests/tests.py) invokes the Python and JavaScript implementations of `crossjson()` and `crosshash()` on the same data and compares the results.



## Development

```bash
git clone git@github.com:httpie/crosshash.git
cd crosshash
make install
make test
```
