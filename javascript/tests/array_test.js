import { test} from "node:test"

import { strict as assert } from "node:assert"
import Arr from "../array.js"

test("Array", () => {
    const arr = new Arr([1, 2, 3]);

    // Test append
    arr.append(4);
    assert.deepEqual(arr.arr, [1, 2, 3, 4]);

    // Test prepend
    arr.prepend(0);
    assert.deepEqual(arr.arr, [0, 1, 2, 3, 4]);

    // Test insert
    arr.insert(2, 1.5);
    assert.deepEqual(arr.arr, [0, 1, 1.5, 2, 3, 4]);

    // Test remove
    arr.remove(2);
    assert.deepEqual(arr.arr, [0, 1, 2, 3, 4]);

    // Test get
    assert.equal(arr.get(2), 2);

    // Test set
    arr.set(2, 5);
    assert.deepEqual(arr.arr, [0, 1, 5, 3, 4]);
})

