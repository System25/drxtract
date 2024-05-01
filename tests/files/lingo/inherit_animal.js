class Object__2 extends ObjectBase {
    birth(legs) {
        this.legCount = legs;
        return this;
    }

    countLegs() {
        return this.legCount;
    }
}

function countLegs(obj, ...args) {
    return obj.countLegs(...args);
}
