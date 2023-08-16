function exitFrame() {
    var val;

    val = _movie.beepOn;
    put("beepOn=", val);
    _movie.beepOn = !(val);
}
