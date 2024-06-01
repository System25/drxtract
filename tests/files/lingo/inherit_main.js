function exitFrame() {
    var dragonFly;
    var dog;

    put(new LingoString("Create an insect"));
    dragonFly = _movie.newScript(script(new LingoString("Insect")), 4);
    put(new LingoString("dragonFly.legCount"), dragonFly.legCount);
    put(new LingoString("dragonFly.wingCount"), dragonFly.wingCount);
    put(new LingoString("Create a quadruped"));
    dog = _movie.newScript(script(new LingoString("Quadruped")), 1);
    put(new LingoString("dog.legCount"), dog.legCount);
    put(new LingoString("dog.hasTail"), dog.hasTail);
    put(new LingoString("dog.legCount"), countLegs(dog));
}
