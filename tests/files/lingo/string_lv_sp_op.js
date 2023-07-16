function exitFrame() {
    var myStr;

    put("base item delimiter", _player.itemDelimiter);
    _player.itemDelimiter = ":";
    myStr = "a:b:c";
    put("num of items:", myStr.item.length);
    _player.itemDelimiter = ",";
    put("again:", myStr.item.length);
    myStr.getPropRef("item", 1) = "hey" + myStr.getProp("item", 1);
    put(myStr);
    myStr.getPropRef("item", 1) = myStr.getProp("item", 1) + "you";
    put(myStr);
    myStr.getPropRef("item", 2) = "me";
    put(myStr);
    delete(myStr.getPropRef("item", 1));
    put(myStr);
}
