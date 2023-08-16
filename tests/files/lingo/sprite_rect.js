function exitFrame() {
    put("puppet=", sprite(1).puppet);
    put("rect=", sprite(1).rect);
    sprite(1).rect = rect(0, 0, 120, 100);
}
