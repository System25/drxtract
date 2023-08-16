function exitFrame() {
    var val;

    val = random(10);
    while (val != 3) {
        put("val = ", val);
        val = random(10);
    }
    put("end ;)");
}
