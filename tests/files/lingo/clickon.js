function startMovie() {
    put(new LingoString("clickOn:"), _mouse.clickOn);
    put(new LingoString("doubleClick:"), _mouse.doubleClick);
    put(new LingoString("perFrameHook:"), _system.perFrameHook);
}
