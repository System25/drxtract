function exitFrame() {
    var myName;

    myName = new LingoString("John");
    myName = new LingoString(myName + new LingoString(" Doe"));
    put(myName);
    myName = new LingoString("Doe");
    myName = new LingoString(new LingoString("Janet ") + myName);
    put(myName);
}
