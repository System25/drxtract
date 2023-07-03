function exitFrame() {
    field(2).text = "Hello world!";
    field(3).text = field(2).getProp("word", 2);
    delete(field(2).getPropRef("word", 2));
    put("Field 2: ", field(2));
    put("Field 3: ", member(3).text);
}
