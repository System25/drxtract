function startMovie() {
    var var1;
    var var2;

    var1 = 1;
    var2 = 1;
    if ((var1).valueOf() == 1) {
        if ((var2).valueOf() == 1) {
            put(new LingoString("var 1 and var 2 OK"));
        } else {
            nothing();
        }
    } else {
        put(new LingoString("var 1 KO"));
    }
}
