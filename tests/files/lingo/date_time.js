function exitFrame() {
    put(new LingoString("long date:"), _system.date('long date'));
    put(new LingoString("short date:"), _system.date('short date'));
    put(new LingoString("date:"), _system.date('date'));
    put(new LingoString("abbr date:"), _system.date('abbr date'));
    put(new LingoString("long time:"), _system.date('long time'));
    put(new LingoString("short time:"), _system.date('short time'));
    put(new LingoString("time:"), _system.date('time'));
    put(new LingoString("abbr time:"), _system.date('abbr time'));
}
