function exitFrame() {
    put("backColor: ", member(1).backColor);
    put("center: ", member(1).center);
    put("crop: ", member(1).crop);
    member(1).center = 1;
    member(1).crop = 1;
    put("castType: ", member(1).castType);
    put("depth: ", member(1).depth);
    put("fileName: ", member(1).fileName);
    put("foreColor:", member(1).foreColor);
    put("hilite: ", member(1).hilite);
    put("loaded: ", member(1).loaded);
    put("modified: ", member(1).modified);
    put("name:", member(1).name);
    put("number:", member(1).number);
    put("picture: ", member(1).picture);
    put("preLoad: ", member(1).preLoad);
    put("rect: ", member(1).rect);
    put("scriptText: ", member(1).scriptText);
    put("size: ", member(1).size);
}
