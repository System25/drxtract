function exitFrame() {
    if (_key.commandDown) {
        put("COMMAND");
    }
    if (_key.shiftDown) {
        put("SHIFT");
    }
    if (_key.controlDown) {
        put("CONTROL");
    }
    if (_key.optionDown) {
        put("OPTION");
    }
    put("last key: ", _key.key, " code:", _key.keyCode);
}
