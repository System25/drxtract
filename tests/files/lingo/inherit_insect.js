function birth(me, wings) {
    me.wingCount = wings;
    me.ancestor = _movie.newScript(script("Animal"), 6);
    return me;
}
