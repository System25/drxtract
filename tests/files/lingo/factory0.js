function startMovie() {
    var myStack;
    var myName;

    myStack = makeStack(symbol('mnew'), 1, myStack);
    myStack(symbol('mReset'));
    myName = myStack(symbol('mname'));
    put(new LingoString("name: "), myName);
    myStack(symbol('mPush'), new LingoString("one"));
    myStack(symbol('mPush'), new LingoString("two"));
    myStack(symbol('mPush'), new LingoString("three"));
    put(myStack(symbol('mShow')));
    put(new LingoString("length"), myStack(symbol('mGetLength')));
    put(new LingoString("1"), myStack(symbol('mPull')));
    put(new LingoString("2"), myStack(symbol('mPull')));
    put(new LingoString("3"), myStack(symbol('mPull')));
    put(new LingoString("length"), myStack(symbol('mGetLength')));
}

function dumpObject(whichObject) {
    if (objectp(whichObject)) {
        whichObject(symbol('mRelease'));
        whichObject(symbol('mdispose'));
    }
    return whichObject;
}
