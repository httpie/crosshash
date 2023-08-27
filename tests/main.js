/**
 * Expose JS implementation via CLI.
 */
const {crosshash, crossjson} = require('../crosshash.js')


const main = ({action, inputJson}) => {
    const doHash = {'--json': false, '--hash': true}[action]
    let input = JSON.parse(inputJson)
    return doHash ? crosshash(input) : crossjson(input)
}


console.log(main({action: process.argv[2], inputJson: process.argv[3]}))
