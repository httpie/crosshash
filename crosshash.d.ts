type JSONValue =
    | string
    | number
    | boolean
    | { [x: string]: JSONValue }
    | Array<JSONValue>

export declare function crosshash(obj: JSONValue): string;

export declare function crossjson(obj: JSONValue): string;

export declare class CrossHashError extends Error {}
