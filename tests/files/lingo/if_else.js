function exitFrame() {
    put("------------");
    singleIfTest();
    singleIfElseTest();
    anidatedIfTest();
    put("------------");
}

function singleIfTest() {
    put("Single if test");
    if ((random(10) % 2) == 0) {
        put("Even number!");
    }
    put("Single if test END");
}

function singleIfElseTest() {
    put("Single if-else test");
    if ((random(10) % 2) == 0) {
        put("Even number!");
    } else {
        put("Odd number");
    }
    put("Single if-else test END");
}

function anidatedIfTest() {
    put("Anidated if test");
    if ((random(10) % 2) == 0) {
        if ((random(10) % 2) == 0) {
            put("First even then even");
        } else {
            put("First even then odd");
        }
    } else {
        put("First odd");
        if ((random(10) % 2) == 0) {
            put("Second even");
        }
    }
    put("Anidated if test end");
}
