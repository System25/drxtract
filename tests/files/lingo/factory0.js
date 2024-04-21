function startMovie() {
    var myStack;
    var myName;

    myStack = makeStack(symbol('mnew'), 1, myStack);
    myStack(symbol('mReset'));
    myName = myStack(symbol('mname'));
    put("name: ", myName);
    myStack(symbol('mPush'), "one");
    myStack(symbol('mPush'), "two");
    myStack(symbol('mPush'), "three");
    put(myStack(symbol('mShow')));
    put("length", myStack(symbol('mGetLength')));
    put("1", myStack(symbol('mPull')));
    put("2", myStack(symbol('mPull')));
    put("3", myStack(symbol('mPull')));
    put("length", myStack(symbol('mGetLength')));
}

function dumpObject(whichObject) {
    if (objectp(whichObject)) {
        whichObject(symbol('mRelease'));
        whichObject(symbol('mdispose'));
    }
    return whichObject;
}
