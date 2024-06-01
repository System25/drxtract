function exitFrame() {
    var glist;

    glist = propList(symbol('name'), new LingoString("Jhon"), symbol('surname'), new LingoString("Doe"));
    put(new LingoString("glist="), glist);
    put(new LingoString("name: "), getProp(glist, symbol('name')));
    put(new LingoString("surname:"), getProp(glist, symbol('surname')));
}
