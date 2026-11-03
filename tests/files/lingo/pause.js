function startMovie() {
    put(new LingoString("pause the movie"));
    pause();
    if ((_movie.pauseState).valueOf() == 1) {
        put(new LingoString("the movie was paused"));
        resume();
    }
}
