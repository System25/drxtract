function startMovie() {
    var nlabels;
    var l;
    var thisLabel;

    put(new LingoString("Labels list:"), _movie.labelList);
    put(new LingoString("frameLabel: "), _movie.frameLabel);
    nlabels = _movie.labelList.line.length;
    put(new LingoString("Number of labels: "), nlabels);
    for(l = 1; l <= nlabels; l++) {
        thisLabel = _movie.labelList.line[l];
        put(new LingoString("line: "), l, new LingoString("label:"), thisLabel);
        put(new LingoString("frame number:"), label(thisLabel));
    }
    put(new LingoString("marker(-1):"), marker(-(1)));
    put(new LingoString("marker(0):"), marker(0));
    put(new LingoString("marker(1):"), marker(1));
    put(new LingoString("go square"));
    _movie.go(new LingoString("square"));
    put(new LingoString("marker(-1):"), marker(-(1)));
    put(new LingoString("marker(0):"), marker(0));
    put(new LingoString("marker(1):"), marker(1));
    put(new LingoString("go rounded square"));
    _movie.go(new LingoString("rounded square"));
    put(new LingoString("marker(-1):"), marker(-(1)));
    put(new LingoString("marker(0):"), marker(0));
    put(new LingoString("marker(1):"), marker(1));
}
