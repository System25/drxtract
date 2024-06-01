function mouseUp() {
    open(window(new LingoString("tour")));
    with (window(new LingoString("tour"))) {
        puppetTempo(5);
    }
    with (window(new LingoString("tour"))) {
        go(1);
        stageColor = 0;
        updateStage();
    }
}
