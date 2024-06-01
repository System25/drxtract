function exitFrame() {
    if (sprite(1).intersects(sprite(2))) {
        put(new LingoString("The sprite 1 intersects sprite 2"));
    } else {
        put(new LingoString("The sprite1 does not intersects sprite 2"));
    }
}
