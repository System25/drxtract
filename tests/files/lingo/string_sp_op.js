function exitFrame() {
    var myLocalVar;
    var myAbcs;

    myLocalVar = field(2).text;
    put(new LingoString("Number of chars: "), myLocalVar.char.length);
    put(new LingoString("First char: "), myLocalVar.getProp("char", 1));
    put(new LingoString("Last char: "), myLocalVar.getProp("char", 62));
    put(new LingoString("Number of words: "), myLocalVar.word.length);
    put(new LingoString("First word: "), myLocalVar.getProp("word", 1));
    put(new LingoString("Last word: "), myLocalVar.getProp("word", 12));
    put(new LingoString("Number of lines: "), myLocalVar.line.length);
    put(new LingoString("First line: "), myLocalVar.getProp("line", 1));
    put(new LingoString("Last line: "), myLocalVar.getProp("line", 2));
    put(new LingoString("2,2,2="), myLocalVar.getPropRef("line", 2).getPropRef("word", 2).getProp("char", 2));
    put(new LingoString("Number of items: "), myLocalVar.item.length);
    put(new LingoString("First item: "), myLocalVar.getProp("item", 1));
    put(new LingoString("2, 2, 2, 2="), myLocalVar.getPropRef("line", 2).getPropRef("item", 1).getPropRef("word", 2).getProp("char", 2));
    myAbcs = new LingoString("ABCDEFGHIJKLMNOPQRSTUVWXYZ");
    put(new LingoString("char 2,4 = "), myAbcs.getProp("char", 2, 4));
    put(new LingoString("word 2, 4 = "), myLocalVar.getProp("word", 2, 4));
    put(new LingoString("lines 1,2 = "), myLocalVar.getProp("line", 1, 2));
    put(new LingoString("items 1, 1="), myLocalVar.getProp("item", 1, 1));
}
