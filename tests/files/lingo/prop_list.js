function exitFrame() {
    var myPropList;

    myPropList = propList();
    put("Empty prop list: ", myPropList);
    addProp(myPropList, symbol('name'), "Jhon");
    addProp(myPropList, symbol('surname'), "Doe");
    put("Full prop list: ", myPropList);
    deleteProp(myPropList, symbol('surname'));
    put("Only name", myPropList);
}
