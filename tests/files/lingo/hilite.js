function mouseUp() {
    var value;

    value = member(4).hilite;
    put(new LingoString("hilite is: "), value);
    member(4).hilite = !(value);
}
