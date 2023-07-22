function exitFrame() {
    put("textAlign: ", field(1).textAlign);
    member(1).textAlign = "right";
    put("textAlign: ", field(1).textAlign);
    put("textFont: ", field(1).textFont);
    member(1).textFont = "Times";
    put("textFont: ", field(1).textFont);
    put("textHeight: ", field(1).textHeight);
    member(1).textHeight = 14;
    put("textHeight: ", field(1).textHeight);
    put("textSize:", field(1).textSize);
    member(1).textSize = 10;
    put("textSize: ", field(1).textSize);
    put("textStyle:", field(1).textStyle);
    member(1).textStyle = "bold";
    put("textStyle: ", field(1).textStyle);
}
