function exitFrame() {
    var dragonFly;
    var dog;

    put("Create an insect");
    dragonFly = _movie.newScript(script("Insect"), 4);
    put("dragonFly.legCount", dragonFly.legCount);
    put("dragonFly.wingCount", dragonFly.wingCount);
    put("Create a quadruped");
    dog = _movie.newScript(script("Quadruped"), 1);
    put("dog.legCount", dog.legCount);
    put("dog.hasTail", dog.hasTail);
    put("dog.legCount", countLegs(dog));
}
