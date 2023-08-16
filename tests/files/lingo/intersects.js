function exitFrame() {
    if (sprite(1).intersects(sprite(2))) {
        put("The sprite 1 intersects sprite 2");
    } else {
        put("The sprite1 does not intersects sprite 2");
    }
}
