function exitFrame() {
    put("base item delimiter", _player.itemDelimiter);
    _player.itemDelimiter = ":";
    field(2).text = "a:b:c";
    put("num of items:", field(2).item.length);
    _player.itemDelimiter = ",";
    put("again:", field(2).item.length);
    field(2).text.getPropRef("item", 1) = "hey" + field(2).text.getProp("item", 1);
    put(field(2));
    field(2).text.getPropRef("item", 1) = field(2).text.getProp("item", 1) + "you";
    put(field(2));
    field(2).text.getPropRef("item", 2) = "me";
    put(field(2));
    delete(field(2).getPropRef("item", 1));
    put(field(2));
}
