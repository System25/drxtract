function exitFrame() {
    put(new LingoString("locV: "), sprite(1).locV);
    put(new LingoString("locH:"), sprite(1).locH);
    put(new LingoString("left: "), sprite(1).left);
    put(new LingoString("top: "), sprite(1).top);
    put(new LingoString("right: "), sprite(1).right);
    put(new LingoString("bottom: "), sprite(1).bottom);
    put(new LingoString("width: "), sprite(1).width);
    put(new LingoString("height: "), sprite(1).height);
    put(new LingoString("fore color: "), sprite(1).foreColor);
    put(new LingoString("bg color: "), sprite(1).backColor);
    put(new LingoString("cast fore color"), member(1).foreColor);
    put(new LingoString("cast bg color"), member(1).backColor);
    sprite(1).locV = 10;
    sprite(1).locH = 10;
    member(1).foreColor = 1;
}
