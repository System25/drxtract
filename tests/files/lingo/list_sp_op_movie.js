function startMovie() {
    _global.gList = list();
    _global.gList = new LingoString("you");
    _global.gList.getPropRef("item", 1) = _global.gList.getProp("item", 1) + new LingoString(" man!");
    _global.gList.getPropRef("item", 1) = new LingoString("hey ") + _global.gList.getProp("item", 1);
    _global.gList.getPropRef("item", 2) = new LingoString("hello world!");
    put(new LingoString("======"));
    put(new LingoString("list:"), _global.gList);
    put(new LingoString("======"));
}
