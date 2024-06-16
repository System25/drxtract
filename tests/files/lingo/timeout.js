function startMovie() {
    put(new LingoString("timeoutKeydown:"), _system.timeoutKeyDown);
    put(new LingoString("timeoutMouse:"), _system.timeoutMouse);
    put(new LingoString("timeoutPlay:"), _system.timeoutPlay);
    put(new LingoString("timeoutLength:"), _system.timeoutLength);
    put(new LingoString("timeoutLapsed:"), _system.timeoutLapsed);
    _system.timeoutScript = new LingoString(" put \"Timeout reached!\"\r");
}
