function startMovie() {
    _global.gList = list();
    _global.gList = "you";
    _global.gList.getPropRef("item", 1) = _global.gList.getProp("item", 1) + " man!";
    _global.gList.getPropRef("item", 1) = "hey " + _global.gList.getProp("item", 1);
    _global.gList.getPropRef("item", 2) = "hello world!";
    put("======");
    put("list:", _global.gList);
    put("======");
}
