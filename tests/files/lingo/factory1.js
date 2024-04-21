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
        return "Stack:Factory";
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

        put("** makeStack: mShow");
        put(("Stack length:" + " " + this.myLength));
        for(i = 1; i <= this.myLength; i++) {
            value = this.mget(i);
            if (objectp(value)) {
                value = value(symbol('mname'));
            }
            put(((("Stack position" + " " + i) + " " + ":") + " " + value));
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
