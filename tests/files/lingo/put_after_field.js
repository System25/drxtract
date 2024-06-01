function exitFrame() {
    field(2).text = new LingoString("hello");
    field(2).text = new LingoString(field(2).text + new LingoString(" world"));
    put(field(2));
    field(2).text = new LingoString("bye");
    field(2).text = new LingoString(new LingoString("hello and ") + field(2).text);
    put(field(2));
}
