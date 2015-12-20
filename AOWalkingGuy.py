import pygame, AnimatedObject, animations, images, events


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
        self.setBitmap(images.getImage("walking-guy"))
        self.setAnimation(animations.getAnimation("walking-guy-walk-left"))
        self.setNumberOfLoops(-1)
        self.setFrameRate(20)
        self.play()

        events.bindKeyAxis("a", "d", self.moveRight)
        events.bindKeyAxis("w", "s", self.moveDown)

    def moveRight(self, e, value):
        if value == 1:
            self.setAnimation(animations.getAnimation("walking-guy-walk-right"))
        elif value == -1:
            self.setAnimation(animations.getAnimation("walking-guy-walk-left"))

        self.setXVelocity(value*100)

    def moveDown(self, e, value):
        if value == 1:
            self.setAnimation(animations.getAnimation("walking-guy-walk-down"))
        elif value == -1:
            self.setAnimation(animations.getAnimation("walking-guy-walk-up"))
        self.setYVelocity(value*100)

    def tick(self, delta):
        super(AOWalkingGuy, self).tick(delta)
        if not self.velocity[0] == 0 or not self.velocity[1] == 0:
            self.position[0] += self.velocity[0] * delta
            self.position[1] += self.velocity[1] * delta
        else:
            self.setAnimation(animations.getAnimation("walking-guy-standing"))
