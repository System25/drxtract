function exitFrame() {
    member(2).text = new LingoString("hello");
    member(2).text = new LingoString(member(2).text + new LingoString(" world"));
    put(field(2));
    member(2).text = new LingoString("bye");
    member(2).text = new LingoString(new LingoString("hello and ") + member(2).text);
    put(field(2));
}
