function exitFrame() {
    put(new LingoString("base item delimiter"), _player.itemDelimiter);
    _player.itemDelimiter = new LingoString(":");
    _global.myStr = new LingoString("a:b:c");
    put(new LingoString("num of items:"), _global.myStr.item.length);
    _player.itemDelimiter = new LingoString(",");
    put(new LingoString("again:"), _global.myStr.item.length);
    _global.myStr.getPropRef("item", 1) = new LingoString("hey") + _global.myStr.getProp("item", 1);
    put(_global.myStr);
    _global.myStr.getPropRef("item", 1) = _global.myStr.getProp("item", 1) + new LingoString("you");
    put(_global.myStr);
    _global.myStr.getPropRef("item", 2) = new LingoString("me");
    put(_global.myStr);
    delete(_global.myStr.getPropRef("item", 1));
    put(_global.myStr);
}
