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
    member("Fish.mov").center = 0;
    member("Fish.mov").crop = 0;
    MyDuration = member("Fish.mov").duration;
    MyFrameRate = member("Fish.mov").frameRate;
    MyLoop = member("Fish.mov").loop;
    MyPausedAtStart = member("Fish.mov").pausedAtStart;
    MyPreload = member("Fish.mov").preLoad;
    MyVideo = member("Fish.mov").video;
    MySound = member("Fish.mov").sound;
    put("MyDuration=", MyDuration);
}
