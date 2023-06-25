function exitFrame() {
    put("locV: ", sprite(1).locV);
    put("locH:", sprite(1).locH);
    put("left: ", sprite(1).left);
    put("top: ", sprite(1).top);
    put("right: ", sprite(1).right);
    put("bottom: ", sprite(1).bottom);
    put("width: ", sprite(1).width);
    put("height: ", sprite(1).height);
    put("fore color: ", sprite(1).foreColor);
    put("bg color: ", sprite(1).backColor);
    put("cast fore color", member(1).foreColor);
    put("cast bg color", member(1).backColor);
    sprite(1).locV = 10;
    sprite(1).locH = 10;
    member(1).foreColor = 1;
}
