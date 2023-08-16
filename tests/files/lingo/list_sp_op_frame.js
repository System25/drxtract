function exitFrame() {
    var x;

    put("num of items", _global.gList.item.length);
    x = _global.gList.getProp("item", 1);
    delete(_global.gList.getPropRef("item", 1));
    _global.gList.getPropRef("item", 2) = x;
    put("list: ", _global.gList);
}
