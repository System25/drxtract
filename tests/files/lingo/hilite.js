function mouseUp() {
    var value;

    value = member(4).hilite;
    put("hilite is: ", value);
    member(4).hilite = !(value);
}
