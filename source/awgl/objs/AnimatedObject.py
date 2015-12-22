import pygame, StaticObject

class AnimatedObject(StaticObject.StaticObject):
    def __init__(self):
        super(AnimatedObject, self).__init__()
        self.isPlaying = False
        self.numLoops = -1
        self.frame = 0
        self.fps = 1
        self.animation = None

    def setAnimation(self, animation):
        if not animation is self.animation:
            self.frame = 0
            self.animation = animation

    def getRenderRect(self):
        return self.animation.getFrameRect(int(self.frame)) if self.animation else self.renderRect if self.bitmap else None

    def setNumberOfLoops(self, loops):
        self.numLoops = loops

    def play(self):
        if not self.isPlaying:
            self.frame = 0
            self.isPlaying = True

    def stop(self):
        if self.isPlaying:
            self.isPlaying = False

    def setFrameRate(self, fps):
        self.fps = int(fps)

    def setFrame(self, frame):
        self.frame = frame

    def getSize(self):
        return (self.animation.getFrameRect(int(self.frame)).w, self.animation.getFrameRect(int(self.frame)).h)

    def tick(self, delta):
        super(AnimatedObject, self).tick(delta)
        if self.isPlaying:
            self.frame += (delta * self.fps)
            if self.frame > self.animation.numberOfFrames()-1:
                if self.numLoops > 0:
                    self.numLoops -= 1
                    if self.numLoops == 0:
                        self.isPlaying = False
                self.frame = self.frame % self.animation.numberOfFrames()
