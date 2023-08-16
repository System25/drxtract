function exitFrame() {
    var myLocalVar;
    var myAbcs;

    myLocalVar = field(2).text;
    put("Number of chars: ", myLocalVar.char.length);
    put("First char: ", myLocalVar.getProp("char", 1));
    put("Last char: ", myLocalVar.getProp("char", 62));
    put("Number of words: ", myLocalVar.word.length);
    put("First word: ", myLocalVar.getProp("word", 1));
    put("Last word: ", myLocalVar.getProp("word", 12));
    put("Number of lines: ", myLocalVar.line.length);
    put("First line: ", myLocalVar.getProp("line", 1));
    put("Last line: ", myLocalVar.getProp("line", 2));
    put("2,2,2=", myLocalVar.getPropRef("line", 2).getPropRef("word", 2).getProp("char", 2));
    put("Number of items: ", myLocalVar.item.length);
    put("First item: ", myLocalVar.getProp("item", 1));
    put("2, 2, 2, 2=", myLocalVar.getPropRef("line", 2).getPropRef("item", 1).getPropRef("word", 2).getProp("char", 2));
    myAbcs = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    put("char 2,4 = ", myAbcs.getProp("char", 2, 4));
    put("word 2, 4 = ", myLocalVar.getProp("word", 2, 4));
    put("lines 1,2 = ", myLocalVar.getProp("line", 1, 2));
    put("items 1, 1=", myLocalVar.getProp("item", 1, 1));
}
