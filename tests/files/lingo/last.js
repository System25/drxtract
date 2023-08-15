function exitFrame() {
    var myText;

    myText = "Macromedia director is cool";
    put("last word: ", myText.getProp("word", "last"));
    put("last char:", myText.getProp("char", "last"));
    put("first word:", myText.getProp("word", 1));
    put("last of first:", myText.getProp("word", 1).getProp("char", "last"));
}
