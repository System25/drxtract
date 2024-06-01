function exitFrame() {
    var myPropList;

    myPropList = propList();
    put(new LingoString("Empty prop list: "), myPropList);
    addProp(myPropList, symbol('name'), new LingoString("Jhon"));
    addProp(myPropList, symbol('surname'), new LingoString("Doe"));
    put(new LingoString("Full prop list: "), myPropList);
    deleteProp(myPropList, symbol('surname'));
    put(new LingoString("Only name"), myPropList);
}
