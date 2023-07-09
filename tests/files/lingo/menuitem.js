function startMovie() {
    installMenu(1);
    put("---------");
    put("Number of menus: ", _menuBar.menu.length);
    put("Menu: ", _menuBar.menu[1].name);
    put("Number of menuitems: ", _menuBar.menu[1].item.length);
    put("First menuitem: ", _menuBar.menu[1].item[1].name);
    put("Enabled: ", _menuBar.menu[1].item[1].enabled);
    put("Checkmark: ", _menuBar.menu[1].item[1].checkMark);
    put("Script: ", _menuBar.menu[1].item[1].script);
    _menuBar.menu[1].item[1].name = "hello";
    _menuBar.menu[1].item[1].enabled = 0;
    _menuBar.menu[1].item[1].checkMark = 1;
    _menuBar.menu[1].item[2].script = "myscript";
}

function myscript() {
    put("My script is executed");
}
