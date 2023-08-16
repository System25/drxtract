function exitFrame() {
    _movie.goLoop();
}

function keyDown() {
    put("In frame 1, key = ", _key.key);
    if (_key.key == "n") {
        _movie.goNext();
    }
    if (_key.key == "p") {
        _movie.goPrevious();
    }
    if (_key.key == "1") {
        _movie.go(1);
    }
}
