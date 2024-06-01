function exitFrame() {
    var myName;

    myName = new LingoString("John");
    myName = myName + new LingoString(" Doe");
    put(myName);
    myName = new LingoString("Doe");
    myName = new LingoString("Janet ") + myName;
    put(myName);
}
