function mouseUp() {
    open(window("tour"));
    with (window("tour")) {
        puppetTempo(5);
    }
    with (window("tour")) {
        go(1);
        stageColor = 0;
        updateStage();
    }
}
