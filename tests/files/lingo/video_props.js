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
    MyDuration = member("Fish.mov").duration;
    MyFrameRate = cast("Fish.mov").frameRate;
    MyLoop = member("Fish.mov").loop;
    MyPausedAtStart = cast("Fish.mov").pausedAtStart;
    MyPreload = cast("Fish.mov").preLoad;
    MyVideo = cast("Fish.mov").video;
    MySound = member("Fish.mov").sound;
    put("MyDuration=", MyDuration);
}
