function exitFrame() {
    if (_key.commandDown) {
        put(new LingoString("COMMAND"));
    }
    if (_key.shiftDown) {
        put(new LingoString("SHIFT"));
    }
    if (_key.controlDown) {
        put(new LingoString("CONTROL"));
    }
    if (_key.optionDown) {
        put(new LingoString("OPTION"));
    }
    put(new LingoString("last key: "), _key.key, new LingoString(" code:"), _key.keyCode);
}
