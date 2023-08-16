function startMovie() {
    sound(symbol('playFile'), 1, "Start");
    sound(symbol('fadeIn'), 1);
    put("soundBusy: ", soundBusy(1));
    sound(symbol('fadeOut'), 2);
    sound(symbol('stop'), 1);
    sound(symbol('close'), 1);
    put("soundBusy:", soundBusy(1));
}
