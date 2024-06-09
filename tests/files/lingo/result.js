function startMovie() {
    var three;

    put(new LingoString("before start"));
    put(_player.result);
    put(new LingoString("call myfunc"));
    fn_call(myfunc());
    put(new LingoString("two:"), (1 + 1));
    fn_call(myOtherFunc());
    put(_player.result);
    three = threefunc();
    put(new LingoString("three:"), three);
    put(_player.result);
    fn_call(threefunc());
    put(new LingoString("three:"), _player.result);
}

function threefunc() {
    return 3;
}

function myfunc() {
    return new LingoString("my result");
}

function myOtherFunc() {
    put(new LingoString("inside myOtherFunc"));
}
