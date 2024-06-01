function exitFrame() {
    put(new LingoString("beepOn: "), _movie.beepOn);
    put(new LingoString("buttonStyle: "), _movie.buttonStyle);
    put(new LingoString("centerStage: "), _movie.centerStage);
    put(new LingoString("checkBoxAccess: "), _system.checkBoxAccess);
    put(new LingoString("checkBoxType: "), _system.checkBoxType);
    put(new LingoString("colorDepth: "), _system.colorDepth);
    put(new LingoString("exitLock:"), _movie.exitLock);
    put(new LingoString("fixStageSize: "), _movie.fixStageSize);
    put(new LingoString("soundEnabled: "), _sound.soundEnabled);
    put(new LingoString("soundLevel: "), _sound.soundLevel);
    put(new LingoString("stageColor:"), _movie.stageColor);
    put(new LingoString("stillDown: "), _key.stillDown);
    put(new LingoString("timeoutKeyDown:"), _system.timeoutKeyDown);
    put(new LingoString("timeoutLength:"), _system.timeoutLength);
    put(new LingoString("timeoutMouse:"), _system.timeoutMouse);
    put(new LingoString("timeoutPlay:"), _system.timeoutPlay);
    put(new LingoString("timer: "), _system.timer);
    put(new LingoString("switchColorDepth:"), _player.switchColorDepth);
    put(new LingoString("updateMovieEnabled: "), _movie.updateMovieEnabled);
}
