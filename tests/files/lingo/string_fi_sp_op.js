function exitFrame() {
    put(new LingoString("base item delimiter"), _player.itemDelimiter);
    _player.itemDelimiter = new LingoString(":");
    field(2).text = new LingoString("a:b:c");
    put(new LingoString("num of items:"), field(2).item.length);
    _player.itemDelimiter = new LingoString(",");
    put(new LingoString("again:"), field(2).item.length);
    field(2).text.item[1] = new LingoString("hey") + field(2).text.item[1];
    put(field(2));
    field(2).text.item[1] = field(2).text.item[1] + new LingoString("you");
    put(field(2));
    field(2).text.item[2] = new LingoString("me");
    put(field(2));
    delete(field(2).item[1]);
    put(field(2));
}
