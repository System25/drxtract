function exitFrame() {
    var myStr;

    put(new LingoString("base item delimiter"), _player.itemDelimiter);
    _player.itemDelimiter = new LingoString(":");
    myStr = new LingoString("a:b:c");
    put(new LingoString("num of items:"), myStr.item.length);
    _player.itemDelimiter = new LingoString(",");
    put(new LingoString("again:"), myStr.item.length);
    myStr.item[1] = new LingoString(new LingoString("hey") + myStr.item[1]);
    put(myStr);
    myStr.item[1] = new LingoString(myStr.item[1] + new LingoString("you"));
    put(myStr);
    myStr.item[2] = new LingoString("me");
    put(myStr);
    delete(myStr.item[1]);
    put(myStr);
}
