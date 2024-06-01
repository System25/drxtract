function startMovie() {
    put(new LingoString("contains operator examples"));
    put(new LingoString("Hey man!").contains(new LingoString("MAN")));
    put(new LingoString("Hey man!").contains(new LingoString("man")));
    put(new LingoString("Hey man!").contains(new LingoString("woman")));
    put(new LingoString("Hey man!").contains(new LingoString("!")));
    put(new LingoString("Hey m\xc5n!").contains(new LingoString("man")));
    put(new LingoString("starts operator examples"));
    put(new LingoString("Man and woman").start(new LingoString("MAN")));
    put(new LingoString("Man and woman").start(new LingoString("man")));
    put(new LingoString("Man and woman ").start(new LingoString("woman")));
    put(new LingoString("m\xc5n and woman").start(new LingoString("man")));
    put(new LingoString("offset operator examples"));
    put(offset(new LingoString("man"), new LingoString("My WOMAN")));
    put(offset(new LingoString("dog"), new LingoString("My cat")));
    put(offset(new LingoString("m\xc5n"), new LingoString("My WOMAN")));
    put(new LingoString("length function examples"));
    put(length(new LingoString("")));
    put(length(new LingoString("a")));
    put(length(new LingoString("hey man!")));
}
