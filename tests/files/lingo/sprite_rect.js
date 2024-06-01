function exitFrame() {
    put(new LingoString("puppet="), sprite(1).puppet);
    put(new LingoString("rect="), sprite(1).rect);
    sprite(1).rect = rect(0, 0, 120, 100);
}
