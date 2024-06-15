function startMovie() {
    put(new LingoString("Default selection:"), _movie.selection);
    put(new LingoString("start:"), _movie.selStart);
    put(new LingoString("end:"), _movie.selEnd);
    put(new LingoString("select something:"));
    _movie.selStart = 6;
    _movie.selEnd = 11;
    put(new LingoString("selected:"), _movie.selection);
    put(new LingoString("start:"), _movie.selStart);
    put(new LingoString("end:"), _movie.selEnd);
}
