function exitFrame() {
    _movie.goLoop();
}

function keyDown() {
    put(new LingoString("In frame 1, key = "), _key.key);
    if (_key.key == new LingoString("n")) {
        _movie.goNext();
    }
    if (_key.key == new LingoString("p")) {
        _movie.goPrevious();
    }
    if (_key.key == new LingoString("1")) {
        _movie.go(1);
    }
}
