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
    if (!Number.isSafeInteger(value)) {
        throw new CrossHashError(`${ERROR_UNSAFE_NUMBER}: ${value}`)
    }
}

module.exports = {
    crosshash,
    crossjson,
    CrossHashError,
}
