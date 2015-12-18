import pygame, events

class StaticObject:

    def __init__(self, shouldTick=True):
        self.bitmap = None
        self.position = [0,0]
        self.size = [0,0]
        self.velocity = [0,0]
        self._isValid = True

        if shouldTick:
            events.registerTickableObject(self)

    def setBitmap(self, surface):
        self.size = [surface.get_width(), surface.get_height()]
        self.bitmap = surface

    def getBitmap(self):
        return self.bitmap

    def getPosition(self):
        return self.position

    def move(self, deltaX, deltaY):
        self.position = [self.position[0]+deltaX, self.position[1]+deltaY]

    def setVelocity(self, velocityX, velocityY):
        self.velocity = [velocityX, velocityY]

    def tick(self, delta):
        self.position = [self.position[0] + self.velocity[0], self.position[1] + self.velocity[1]]
