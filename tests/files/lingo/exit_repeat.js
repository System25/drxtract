function exitFrame() {
    var i;

    put("Start!");
    for(i = 1; i <= 10; i++) {
        put("i=", i);
        if (i == 5) {
            put("Exit repeat!");
            break;
        }
    }
    put("End!");
}
