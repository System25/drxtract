function exitFrame() {
    var val;

    put("1 to 10...");
    for(val = 1; val <= 10; val++) {
        put("val=", val);
    }
    put("10 to 1...");
    for(val = 10; val >= 1; val--) {
        put("val=", val);
    }
    put("In list...");
    for(val of list(2, 4, 6, 8, 10)) {
        put("val=", val);
    }
}
