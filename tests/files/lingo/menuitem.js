function startMovie() {
    installMenu(1);
    put(new LingoString("---------"));
    put(new LingoString("Number of menus: "), _menuBar.menu.length);
    put(new LingoString("Menu: "), _menuBar.menu[1].name);
    put(new LingoString("Number of menuitems: "), _menuBar.menu[1].item.length);
    put(new LingoString("First menuitem: "), _menuBar.menu[1].item[1].name);
    put(new LingoString("Enabled: "), _menuBar.menu[1].item[1].enabled);
    put(new LingoString("Checkmark: "), _menuBar.menu[1].item[1].checkMark);
    put(new LingoString("Script: "), _menuBar.menu[1].item[1].script);
    _menuBar.menu[1].item[1].name = new LingoString("hello");
    _menuBar.menu[1].item[1].enabled = 0;
    _menuBar.menu[1].item[1].checkMark = 1;
    _menuBar.menu[1].item[2].script = new LingoString("myscript");
}

function myscript() {
    put(new LingoString("My script is executed"));
}
