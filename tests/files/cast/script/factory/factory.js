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

function mnew(me, masterObject, theObject) {
    me.myMaster = masterObject;
    theObject = dumpObject(theObject);
    me.myLength = 0;
    me(symbol('mReset'));
}

function mReset(me) {
    var i;

    for(i = 1; i <= me.myLength; i++) {
        me(symbol('mput'), i, 0);
    }
    me.myLength = 0;
}

function mname(me) {
    return "Stack:Factory";
}

function mPush(me, value) {
    me.myLength = (me.myLength + 1);
    me(symbol('mput'), me.myLength, value);
}

function mPop(me) {
    var value;

    if (me.myLength > 0) {
        value = me(symbol('mget'), me.myLength);
        me.myLength = (me.myLength - 1);
        return value;
    } else {
        return symbol('StackUnderflow');
    }
}

function mPull(me) {
    var value;

    if (me.myLength > 0) {
        value = me(symbol('mget'), 1);
        me(symbol('mRemove'), 1);
        return value;
    } else {
        return symbol('StackUnderflow');
    }
}

function mRemove(me, position) {
    var i;

    if (((me.myLength > 0) && (position > 0)) && (position <= me.myLength)) {
        for(i = position; i <= (me.myLength - 1); i++) {
            me(symbol('mput'), i, me(symbol('mget'), (i + 1)));
        }
        me.myLength = (me.myLength - 1);
    }
}

function mGetLength(me) {
    return me.myLength;
}

function mPutLength(me, whatLength) {
    me.myLength = whatLength;
}

function mShow(me) {
    var i;
    var value;

    put("** makeStack: mShow");
    put(("Stack length:" + " " + me.myLength));
    for(i = 1; i <= me.myLength; i++) {
        value = me(symbol('mget'), i);
        if (objectp(value)) {
            value = value(symbol('mname'));
        }
        put(((("Stack position" + " " + i) + " " + ":") + " " + value));
    }
}

function mRelease(me) {
    var i;

    if (me.myMaster) {
        for(i = 1; i <= me.myLength; i++) {
            me(symbol('mput'), i, dumpObject(me(symbol('mget'), i)));
        }
        me.myLength = 0;
    } else {
        me(symbol('mReset'));
    }
}
