function exitFrame() {
    var myText;

    myText = new LingoString("Macromedia director is cool");
    put(new LingoString("last word: "), myText.getProp("word", "last"));
    put(new LingoString("last char:"), myText.getProp("char", "last"));
    put(new LingoString("first word:"), myText.getProp("word", 1));
    put(new LingoString("last of first:"), myText.getProp("word", 1).getProp("char", "last"));
}
