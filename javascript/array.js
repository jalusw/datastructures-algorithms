export default class Arr{
    constructor(arr = []){
        this.arr = arr;
    }

    append(value){
        this.arr.push(value);
    }

    prepend(value){
        this.arr.unshift(value);
    }

    insert(index, value){
        this.arr.splice(index, 0, value);
    }

    remove(index){
        this.arr.splice(index, 1);
    }

    get(index){
        return this.arr[index];
    }

    set(index, value){
        this.arr[index] = value;
    }
}

