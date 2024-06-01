function exitFrame() {
    put(new LingoString("volume: "), sound(1).volume);
    sound(1).volume = 200;
}
