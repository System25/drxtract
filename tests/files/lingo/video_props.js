function mouseUp() {
    var MyDuration;
    var MyFrameRate;
    var MyLoop;
    var MyPausedAtStart;
    var MyPreload;
    var MyVideo;
    var MySound;

    member("Fish.mov").directToStage = 1;
    member("Fish.mov").controller = 1;
    member(new LingoString("Fish.mov")).center = 0;
    member(new LingoString("Fish.mov")).crop = 0;
    MyDuration = member("Fish.mov").duration;
    MyFrameRate = member(new LingoString("Fish.mov")).frameRate;
    MyLoop = member("Fish.mov").loop;
    MyPausedAtStart = member(new LingoString("Fish.mov")).pausedAtStart;
    MyPreload = member(new LingoString("Fish.mov")).preLoad;
    MyVideo = member(new LingoString("Fish.mov")).video;
    MySound = member("Fish.mov").sound;
    put(new LingoString("MyDuration="), MyDuration);
}
