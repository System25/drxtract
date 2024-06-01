function exitFrame() {
    var val;

    put(new LingoString("1 to 10..."));
    for(val = 1; val <= 10; val++) {
        put(new LingoString("val="), val);
    }
    put(new LingoString("10 to 1..."));
    for(val = 10; val >= 1; val--) {
        put(new LingoString("val="), val);
    }
    put(new LingoString("In list..."));
    for(val of list(2, 4, 6, 8, 10)) {
        put(new LingoString("val="), val);
    }
}
