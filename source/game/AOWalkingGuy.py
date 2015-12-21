import pygame, random
from ..awgl.modules import *
from ..awgl.objs import *

animations.addAnimation("walking-guy-walk-left", [(64*i, 64, 64, 64) for i in range(9)])
animations.addAnimation("walking-guy-walk-up", [(64*i, 0, 64, 64) for i in range(9)])
animations.addAnimation("walking-guy-walk-right", [(64*i, 192, 64, 64) for i in range(9)])
animations.addAnimation("walking-guy-walk-down", [(64*i, 128, 64, 64) for i in range(9)])
animations.addAnimation("walking-guy-standing", [(64*i, 128, 64, 64) for i in range(1)])

images.addToGlobalLoadList([
    ("walking-guy", "guy-walk.png")
])

class AOWalkingGuy(AnimatedObject.AnimatedObject):
    def __init__(self, controllerId=0):
        super(AOWalkingGuy, self).__init__()
        self.walkingSpeed = random.randint(100, 150)
        self.walkingFPS = random.randint(30, 45)
        self.currentSpeed = self.walkingSpeed
        self.maxFPS = self.walkingFPS

        self.setBitmap(images.getImage("walking-guy"))
        self.setAnimation(animations.getAnimation("walking-guy-walk-left"))
        self.setNumberOfLoops(-1)
        self.setFrameRate(self.walkingFPS)
        self.play()

        if controllerId == 0:
            events.bindKeyAxis("a", "d", self.moveRight)
            events.bindKeyAxis("w", "s", self.moveDown)

        events.bindJoystickAxisMotionEvent(controllerId, 0, self.moveRight)
        events.bindJoystickAxisMotionEvent(controllerId, 1, self.moveDown)
        events.bindJoystickButtonAxis(controllerId, 1, 0, lambda e, v: self.modifyWalkingSpeed(v))

    def moveRight(self, e, value):
        self.setXVelocity(value)

    def moveDown(self, e, value):
        self.setYVelocity(value)

    def modifyWalkingSpeed(self, value):
        self.currentSpeed = self.walkingSpeed + 80 * value
        self.maxFPS = self.walkingFPS + 15 * value

    def updateMoveAnimation(self):
        if abs(self.velocity[0]) > abs(self.velocity[1]):
            self.setFrameRate(abs(self.velocity[0])*self.maxFPS)
            if self.velocity[0] > 0:
                self.setAnimation(animations.getAnimation("walking-guy-walk-right"))
            else:
                self.setAnimation(animations.getAnimation("walking-guy-walk-left"))
        else:
            self.setFrameRate(abs(self.velocity[1])*self.maxFPS)
            if self.velocity[1] > 0:
                self.setAnimation(animations.getAnimation("walking-guy-walk-down"))
            else:
                self.setAnimation(animations.getAnimation("walking-guy-walk-up"))

    def tick(self, delta):
        super(AOWalkingGuy, self).tick(delta)
        if not self.velocity[0] == 0 or not self.velocity[1] == 0:
            self.updateMoveAnimation()
            self.position[0] += self.velocity[0] * delta * self.currentSpeed
            self.position[1] += self.velocity[1] * delta * self.currentSpeed
        else:
            #self.setAnimation(animations.getAnimation("walking-guy-standing"))
            self.setFrameRate(0)
