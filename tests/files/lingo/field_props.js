function exitFrame() {
    put(new LingoString("textAlign: "), field(1).textAlign);
    member(1).textAlign = new LingoString("right");
    put(new LingoString("textAlign: "), field(1).textAlign);
    put(new LingoString("textFont: "), field(1).textFont);
    member(1).textFont = new LingoString("Times");
    put(new LingoString("textFont: "), field(1).textFont);
    put(new LingoString("textHeight: "), field(1).textHeight);
    member(1).textHeight = 14;
    put(new LingoString("textHeight: "), field(1).textHeight);
    put(new LingoString("textSize:"), field(1).textSize);
    member(1).textSize = 10;
    put(new LingoString("textSize: "), field(1).textSize);
    put(new LingoString("textStyle:"), field(1).textStyle);
    member(1).textStyle = new LingoString("bold");
    put(new LingoString("textStyle: "), field(1).textStyle);
}
