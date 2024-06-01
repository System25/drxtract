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

class Factory__makeStack extends FactoryBase {
    mnew(masterObject, theObject) {
        this.myMaster = masterObject;
        theObject = dumpObject(theObject);
        this.myLength = 0;
        this.mReset();
    }

    mReset() {
        var i;

        for(i = 1; i <= this.myLength; i++) {
            this.mput(i, 0);
        }
        this.myLength = 0;
    }

    mname() {
        return new LingoString("Stack:Factory");
    }

    mPush(value) {
        this.myLength = (this.myLength + 1);
        this.mput(this.myLength, value);
    }

    mPop() {
        var value;

        if (this.myLength > 0) {
            value = this.mget(this.myLength);
            this.myLength = (this.myLength - 1);
            return value;
        } else {
            return symbol('StackUnderflow');
        }
    }

    mPull() {
        var value;

        if (this.myLength > 0) {
            value = this.mget(1);
            this.mRemove(1);
            return value;
        } else {
            return symbol('StackUnderflow');
        }
    }

    mRemove(position) {
        var i;

        if (((this.myLength > 0) && (position > 0)) && (position <= this.myLength)) {
            for(i = position; i <= (this.myLength - 1); i++) {
                this.mput(i, this.mget((i + 1)));
            }
            this.myLength = (this.myLength - 1);
        }
    }

    mGetLength() {
        return this.myLength;
    }

    mPutLength(whatLength) {
        this.myLength = whatLength;
    }

    mShow() {
        var i;
        var value;

        put(new LingoString("** makeStack: mShow"));
        put((new LingoString("Stack length:") + " " + this.myLength));
        for(i = 1; i <= this.myLength; i++) {
            value = this.mget(i);
            if (objectp(value)) {
                value = value(symbol('mname'));
            }
            put((((new LingoString("Stack position") + " " + i) + " " + new LingoString(":")) + " " + value));
        }
    }

    mRelease() {
        var i;

        if (this.myMaster) {
            for(i = 1; i <= this.myLength; i++) {
                this.mput(i, dumpObject(this.mget(i)));
            }
            this.myLength = 0;
        } else {
            this.mReset();
        }
    }
}

function makeStack(methodName, ...args) {
    return factoryCall('makeStack', methodName, args);
}
