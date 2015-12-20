import pygame, AnimatedObject, animations, images, events, math


animations.addAnimation("walking-guy-walk-left", [(64*i, 64, 64, 64) for i in range(9)])
animations.addAnimation("walking-guy-walk-up", [(64*i, 0, 64, 64) for i in range(9)])
animations.addAnimation("walking-guy-walk-right", [(64*i, 192, 64, 64) for i in range(9)])
animations.addAnimation("walking-guy-walk-down", [(64*i, 128, 64, 64) for i in range(9)])
animations.addAnimation("walking-guy-standing", [(64*i, 128, 64, 64) for i in range(1)])

images.addToGlobalLoadList([
    ("walking-guy", "guy-walk.png")
])

class AOWalkingGuy(AnimatedObject.AnimatedObject):
    def __init__(self):
        super(AOWalkingGuy, self).__init__()
        self.walkingSpeed = 150
        self.maxFPS = 30

        self.setBitmap(images.getImage("walking-guy"))
        self.setAnimation(animations.getAnimation("walking-guy-walk-left"))
        self.setNumberOfLoops(-1)
        self.setFrameRate(20)
        self.play()

        events.bindKeyAxis("a", "d", self.moveRight)
        events.bindKeyAxis("w", "s", self.moveDown)
        events.bindJoystickAxisMotionEvent(0, 0, self.moveRight)
        events.bindJoystickAxisMotionEvent(0, 1, self.moveDown)

    def moveRight(self, e, value):
        self.setXVelocity(value)

    def moveDown(self, e, value):
        self.setYVelocity(value)

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
            self.position[0] += self.velocity[0] * delta * self.walkingSpeed
            self.position[1] += self.velocity[1] * delta * self.walkingSpeed
        else:
            self.setAnimation(animations.getAnimation("walking-guy-standing"))
