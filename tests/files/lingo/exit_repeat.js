function exitFrame() {
    var i;

    put(new LingoString("Start!"));
    for(i = 1; i <= 10; i++) {
        put(new LingoString("i="), i);
        if (i == 5) {
            put(new LingoString("Exit repeat!"));
            break;
        }
    }
    put(new LingoString("End!"));
}
