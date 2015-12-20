import pygame, events

class StaticObject(object):

    def __init__(self):
        self.bitmap = None
        self.position = [0,0]
        self.size = [0,0]
        self.velocity = [0,0]
        self._isValid = True
        self._shouldTick = True

        events.registerTickableObject(self)

    def setBitmap(self, surface):
        self.size = [surface.get_width(), surface.get_height()]
        self.bitmap = surface

    def getBitmap(self):
        return self.bitmap

    def getRenderRect(self):
        return self.bitmap.get_rect() if self.bitmap else None

    def getPosition(self):
        return list(self.position)

    def setPosition(self, x, y):
        self.position = [x, y]

    def addPosition(self, deltaX, deltaY):
        self.position[0] += deltaX
        self.position[1] += deltaY

    def setSize(self, width, height):
        self.size = [width, height]

    def getSize(self):
        return list(self.size)

    def setVelocity(self, velocityX, velocityY):
        self.velocity = [velocityX, velocityY]

    def setXVelocity(self, velocityX):
        self.velocity[0] = velocityX

    def setYVelocity(self, velocityY):
        self.velocity[1] = velocityY

    def addVelocity(self, deltaX, deltaY):
        self.velocity[0] += deltaX
        self.velocity[1] += deltaY

    def getVelocity(self):
        return list(self.velocity)

    def tick(self, delta):
        pass
