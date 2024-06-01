function exitFrame() {
    var myStr;

    put(new LingoString("base item delimiter"), _player.itemDelimiter);
    _player.itemDelimiter = new LingoString(":");
    myStr = new LingoString("a:b:c");
    put(new LingoString("num of items:"), myStr.item.length);
    _player.itemDelimiter = new LingoString(",");
    put(new LingoString("again:"), myStr.item.length);
    myStr.getPropRef("item", 1) = new LingoString("hey") + myStr.getProp("item", 1);
    put(myStr);
    myStr.getPropRef("item", 1) = myStr.getProp("item", 1) + new LingoString("you");
    put(myStr);
    myStr.getPropRef("item", 2) = new LingoString("me");
    put(myStr);
    delete(myStr.getPropRef("item", 1));
    put(myStr);
}
