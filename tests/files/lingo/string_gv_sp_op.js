function exitFrame() {
    put("base item delimiter", _player.itemDelimiter);
    _player.itemDelimiter = ":";
    _global.myStr = "a:b:c";
    put("num of items:", _global.myStr.item.length);
    _player.itemDelimiter = ",";
    put("again:", _global.myStr.item.length);
    _global.myStr.getPropRef("item", 1) = "hey" + _global.myStr.getProp("item", 1);
    put(_global.myStr);
    _global.myStr.getPropRef("item", 1) = _global.myStr.getProp("item", 1) + "you";
    put(_global.myStr);
    _global.myStr.getPropRef("item", 2) = "me";
    put(_global.myStr);
    delete(_global.myStr.getPropRef("item", 1));
    put(_global.myStr);
}
