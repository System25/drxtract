function exitFrame() {
    var x;

    put(new LingoString("num of items"), _global.gList.item.length);
    x = _global.gList.item[1];
    delete(_global.gList.item[1]);
    _global.gList.item[2] = x;
    put(new LingoString("list: "), _global.gList);
}
