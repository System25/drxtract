function exitFrame() {
    var i;

    put(new LingoString("first loop"));
    for(i = 1; i <= 10; i++) {
        put(new LingoString("i="), i);
        if ((i % 2) == 0) {
            put(new LingoString("i is even"));
        } else {
            put(new LingoString("i is odd"));
        }
    }
    put(new LingoString("Second loop"));
    for(i = 1; i <= 10; i++) {
        put(new LingoString("i="), i);
        if (i == 9) {
            break;
        } else {
            put(new LingoString("do not exit yet"));
        }
    }
}
