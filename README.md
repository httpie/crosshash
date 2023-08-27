# `crosshash`

[![Build status](https://github.com/httpie/crosshash/workflows/test/badge.svg)](https://github.com/httpie/crosshash/actions)

Stable, cross-platform JSON serialization and hashing for Python and JavaScript.

## Motivation

To make it possible to compare and hash JSON objects in a stable way across platforms.

## Installation

### Python

[![PyPi](https://badge.fury.io/py/crosshash.svg)](https://pypi.python.org/pypi/crosshash)

```bash
pip install crosshash
```

### JavaScript

[![NPM](https://badge.fury.io/js/crosshash.svg)](https://www.npmjs.com/package/crosshash)

```bash
npm install crosshash
```

## Features

The following features are implemented in both Python and JavaScript and the output is guaranteed to be the same:

### `crossjson(obj) → str`

- Sort keys alphabetically
- Ensure no unsafe numbers are present 
- Serialize using the same format as `JSON.stringify()` (lowest common denominator)

### `crosshash(obj) → str`

- Serialize the object with `crossjson()`
- Hash the resulting string with MD5


## Usage

### Python

#### API

```python
from crosshash import crossjson, crosshash, CrossHashError, MAX_SAFE_INTEGER

obj = {'B': 2, 'C': [1, 2, 3], 'A': 1}

# Generate stable JSON:
assert crossjson(obj) == '{"A":1,"B":2,"C":[1,2,3]}'  

# Generate stable hash:
assert crosshash(obj) == '12982c60a9a8829ea4eeb2e1e7e1e04e'

# Throws `CrossHashError`:
crosshash({'A': MAX_SAFE_INTEGER + 1})  
```

#### CLI

You can invoke `crosshash.py` directly or use `python -m crosshash`. The package also installs an executable `crosshash-py`.

```bash
python3 -m crosshash --json '{"B": 2, "C": [1, 2, 3], "A": 1}'
{"A":1,"B":2,"C":[1,2,3]}
```

```bash
python3 -m crosshash --hash '{"B": 2, "C": [1, 2, 3], "A": 1}'
12982c60a9a8829ea4eeb2e1e7e1e04e
```


### JavaScript

Browsers and Node.js are supported.

#### API

```javascript
const {crossjson, crosshash, CrossHashError} = require('crosshash')

const obj = {'B': 2, 'C': [1, 2, 3], 'A': 1}

// Generate stable JSON:
assert(crossjson(obj) === '{"A":1,"B":2,"C":[1,2,3]}')

// Generate stable hash:
assert(crosshash(obj) === '12982c60a9a8829ea4eeb2e1e7e1e04e')

// Throws `CrossHashError`:
crosshash({A: Number.MAX_SAFE_INTEGER + 1}) 
```

#### CLI

You can invoke `crosshash.js` directly. The package also installs an executable `crosshash-js`.

```bash
./crosshash.js --json '{"B": 2, "C": [1, 2, 3], "A": 1}'
{"A":1,"B":2,"C":[1,2,3]}
```

```bash
./crosshash.js --hash '{"B": 2, "C": [1, 2, 3], "A": 1}'
12982c60a9a8829ea4eeb2e1e7e1e04e
```


## Test suite

To ensure consistency, the [test suite](./tests) invokes the Python and JavaScript implementations of `crossjson()` and `crosshash()` on the [same data](./tests/cases.py) and compares the results.



## Development

It should be fairly straightforward to add support for other languages.

```bash
git clone git@github.com:httpie/crosshash.git
cd ./crosshash
make install
make test
```
