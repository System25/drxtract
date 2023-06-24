function exitFrame() {
    var i;

    put("first loop");
    for(i = 1; i <= 10; i++) {
        put("i=", i);
        if ((i % 2) == 0) {
            put("i is even");
        } else {
            put("i is odd");
        }
    }
    put("Second loop");
    for(i = 1; i <= 10; i++) {
        put("i=", i);
        if (i == 9) {
            break;
        } else {
            put("do not exit yet");
        }
    }
}
