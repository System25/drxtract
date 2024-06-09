function startMovie() {
    put(new LingoString("pause the movie"));
    pause();
    if (_movie.pauseState == 1) {
        put(new LingoString("the movie was paused"));
        resume();
    }
}
