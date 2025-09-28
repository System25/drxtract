function exitFrame() {
    var myLocalVar;
    var myAbcs;

    myLocalVar = field(2);
    put(new LingoString("Number of chars: "), myLocalVar.char.length);
    put(new LingoString("First char: "), myLocalVar.char[1]);
    put(new LingoString("Last char: "), myLocalVar.char[62]);
    put(new LingoString("Number of words: "), myLocalVar.word.length);
    put(new LingoString("First word: "), myLocalVar.word[1]);
    put(new LingoString("Last word: "), myLocalVar.word[12]);
    put(new LingoString("Number of lines: "), myLocalVar.line.length);
    put(new LingoString("First line: "), myLocalVar.line[1]);
    put(new LingoString("Last line: "), myLocalVar.line[2]);
    put(new LingoString("2,2,2="), myLocalVar.line[2].word[2].char[2]);
    put(new LingoString("Number of items: "), myLocalVar.item.length);
    put(new LingoString("First item: "), myLocalVar.item[1]);
    put(new LingoString("2, 2, 2, 2="), myLocalVar.line[2].item[1].word[2].char[2]);
    myAbcs = new LingoString("ABCDEFGHIJKLMNOPQRSTUVWXYZ");
    put(new LingoString("char 2,4 = "), myAbcs.char[range(2, 4)]);
    put(new LingoString("word 2, 4 = "), myLocalVar.word[range(2, 4)]);
    put(new LingoString("lines 1,2 = "), myLocalVar.line[range(1, 2)]);
    put(new LingoString("items 1, 1="), myLocalVar.item[range(1, 1)]);
}
