function exitFrame() {
    put(new LingoString("------------"));
    fn_call(singleIfTest());
    fn_call(singleIfElseTest());
    fn_call(anidatedIfTest());
    put(new LingoString("------------"));
}

function singleIfTest() {
    put(new LingoString("Single if test"));
    if ((random(10) % 2) == 0) {
        put(new LingoString("Even number!"));
    }
    put(new LingoString("Single if test END"));
}

function singleIfElseTest() {
    put(new LingoString("Single if-else test"));
    if ((random(10) % 2) == 0) {
        put(new LingoString("Even number!"));
    } else {
        put(new LingoString("Odd number"));
    }
    put(new LingoString("Single if-else test END"));
}

function anidatedIfTest() {
    put(new LingoString("Anidated if test"));
    if ((random(10) % 2) == 0) {
        if ((random(10) % 2) == 0) {
            put(new LingoString("First even then even"));
        } else {
            put(new LingoString("First even then odd"));
        }
    } else {
        put(new LingoString("First odd"));
        if ((random(10) % 2) == 0) {
            put(new LingoString("Second even"));
        }
    }
    put(new LingoString("Anidated if test end"));
}
