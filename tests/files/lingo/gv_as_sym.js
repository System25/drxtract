function exitFrame() {
    put(new LingoString("Name pos:"), findPos(_global.myList, symbol('name')));
    put(new LingoString("Surname pos:"), findPos(_global.myList, symbol('surname')));
    put(new LingoString("Nothing pos:"), findPos(_global.myList, symbol('nothing')));
    put(new LingoString("Nothing pos near:"), findPosNear(_global.myList, symbol('nothing')));
}
