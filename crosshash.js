#!/usr/bin/env node

const MD5 = require('md5.js')
const stringify = require('json-stable-stringify')

const ERROR_UNSAFE_NUMBER = 'ERROR_UNSAFE_NUMBER'

class CrossHashError extends Error {
    constructor(message) {
        super(message)
        this.name = CrossHashError.name
    }
}

const crosshash = (obj) => {
    return md5(crossjson(obj))
}

const crossjson = (obj) => {
    return stringify(obj, {replacer: replacer})
}

const md5 = (string) => {
    return new MD5().update(string).digest('hex')
}

const replacer = (key, value) => {
    if (typeof value === 'number') {
        validateNumber(value)
    }
    return value
}

const validateNumber = (value) => {
    if (!isSafeNumber(value)) {
        throw new CrossHashError(`${ERROR_UNSAFE_NUMBER}: ${value}`)
    }
}

const isSafeNumber = (value) => {
    return -Number.MAX_SAFE_INTEGER <= value && value <= Number.MAX_SAFE_INTEGER
}

const main = () => {
    const usage = `
    Usage:
        node crosshash.js --json '{"foo": "bar"}'
        node crosshash.js --hash '{"foo": "bar"}'
    `;

    const args = process.argv.slice(2); // remove the first two arguments (node and script name)

    if (args.length !== 2 || !['--json', '--hash'].includes(args[0])) {
        console.log(usage);
        process.exit(1);
    }

    const action = args[0];
    const inputJson = JSON.parse(args[1]);
    const operation = {
        '--json': crossjson,
        '--hash': crosshash
    }[action];

    const output = operation(inputJson);
    return output;
}

if (typeof require !== 'undefined' && typeof module !== 'undefined' && require.main === module) {
    console.log(main())
}


module.exports = {
    crosshash,
    crossjson,
    CrossHashError,
}
