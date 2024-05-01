class Object__3 extends ObjectBase {
    birth(wings) {
        this.wingCount = wings;
        this.ancestor = _movie.newScript(script("Animal"), 6);
        return this;
    }
}

