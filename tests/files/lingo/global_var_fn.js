function exitFrame() {
    _global.myOtherGlobal = 2;
    _global.myGlobalVar = 1;
    put(new LingoString("Begin: "), _global.myGlobalVar);
    func1();
    put(new LingoString("After func1: "), _global.myGlobalVar);
    func2();
    put(new LingoString("After func2: "), _global.myGlobalVar);
}

function func1() {
    _global.myGlobalVar = (_global.myGlobalVar + 1);
}

function func2() {
    _global.myGlobalVar = (_global.myGlobalVar + 1);
}
