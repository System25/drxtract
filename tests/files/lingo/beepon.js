function exitFrame() {
    var val;

    val = _movie.beepOn;
    put(new LingoString("beepOn="), val);
    _movie.beepOn = !(val);
}
