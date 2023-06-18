function exitFrame() {
    field(2).text = "hello";
    field(2).text = field(2).text + " world";
    put(field(2));
    field(2).text = "bye";
    field(2).text = "hello and " + field(2).text;
    put(field(2));
}
