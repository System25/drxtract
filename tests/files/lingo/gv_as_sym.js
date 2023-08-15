function exitFrame() {
    put("Name pos:", findPos(_global.myList, symbol('name')));
    put("Surname pos:", findPos(_global.myList, symbol('surname')));
    put("Nothing pos:", findPos(_global.myList, symbol('nothing')));
    put("Nothing pos near:", findPosNear(_global.myList, symbol('nothing')));
}
