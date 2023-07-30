function exitFrame() {
    var glist;

    glist = propList(symbol('name'), "Jhon", symbol('surname'), "Doe");
    put("glist=", glist);
    put("name: ", getProp(glist, symbol('name')));
    put("surname:", getProp(glist, symbol('surname')));
}
