function exitFrame() {
    var myText;

    myText = new LingoString("Macromedia director is cool");
    put(new LingoString("last word: "), myText.word["last"]);
    put(new LingoString("last char:"), myText.char["last"]);
    put(new LingoString("first word:"), myText.word[1]);
    put(new LingoString("last of first:"), myText.word[1].char["last"]);
}
