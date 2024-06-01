function exitFrame() {
    var val;

    val = random(10);
    while (val != 3) {
        put(new LingoString("val = "), val);
        val = random(10);
    }
    put(new LingoString("end ;)"));
}
