function startMovie() {
    put("contains operator examples");
    put("Hey man!".contains("MAN"));
    put("Hey man!".contains("man"));
    put("Hey man!".contains("woman"));
    put("Hey man!".contains("!"));
    put("Hey m\x81n!".contains("man"));
    put("starts operator examples");
    put("Man and woman".start("MAN"));
    put("Man and woman".start("man"));
    put("Man and woman ".start("woman"));
    put("m\x81n and woman".start("man"));
    put("offset operator examples");
    put(offset("man", "My WOMAN"));
    put(offset("dog", "My cat"));
    put(offset("m\x81n", "My WOMAN"));
    put("length function examples");
    put(length(""));
    put(length("a"));
    put(length("hey man!"));
}
