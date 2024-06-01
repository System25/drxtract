function exitFrame() {
    put(new LingoString("backColor: "), member(1).backColor);
    put(new LingoString("center: "), member(1).center);
    put(new LingoString("crop: "), member(1).crop);
    member(1).center = 1;
    member(1).crop = 1;
    put(new LingoString("castType: "), member(1).castType);
    put(new LingoString("depth: "), member(1).depth);
    put(new LingoString("fileName: "), member(1).fileName);
    put(new LingoString("foreColor:"), member(1).foreColor);
    put(new LingoString("hilite: "), member(1).hilite);
    put(new LingoString("loaded: "), member(1).loaded);
    put(new LingoString("modified: "), member(1).modified);
    put(new LingoString("name:"), member(1).name);
    put(new LingoString("number:"), member(1).number);
    put(new LingoString("picture: "), member(1).picture);
    put(new LingoString("preLoad: "), member(1).preLoad);
    put(new LingoString("rect: "), member(1).rect);
    put(new LingoString("scriptText: "), member(1).scriptText);
    put(new LingoString("size: "), member(1).size);
}
