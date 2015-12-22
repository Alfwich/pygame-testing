import pygame
from ..modules import events

class StaticObject(object):

    def __init__(self):
        self.bitmap = None
        self.position = [0,0]
        self.size = [0,0]
        self.velocity = [0,0]
        self.children = []
        self._isVisible = True
        self._isValid = True
        self._canTick = False
        self._boundEvents = []
        self.renderRect = None
        self.enableTick()

    def _updateRenderRect(self):
        self.renderRect = self.bitmap.get_rect()

    def isVisible(self):
        return self._isVisible

    def setVisibility(self, visibility):
        self._isVisible = visibility

    def addEvents(self, eventIds):
        if not isinstance(eventIds, list):
            eventIds = [eventIds]

        for eventId in eventIds:
            self._boundEvents.append(eventId)

    def disable(self):
        for eventId in self._boundEvents:
            events.unbindEvent(eventId)
        self._boundEvents = []
        self._isValid = False
        self._isVisible = False
        self.disableTick()
        for child in self.children:
            child.disable()

    def enableTick(self):
        if not self._canTick:
            self._canTick = True
            events.registerTickableObject(self)

    def disableTick(self):
        if self._canTick:
            self._canTick = False
            events.deregisterTickableObject(self)

    def setBitmap(self, surface):
        self.size = [surface.get_width(), surface.get_height()]
        self.bitmap = surface
        self._updateRenderRect()

    def scaleBitmap(self, xScale, yScale):
        self.setBitmap(pygame.transform.scale(self.bitmap, (self.bitmap.get_width()*int(xScale), self.bitmap.get_height()*int(yScale))))

    def getBitmap(self):
        return self.bitmap

    def getRenderRect(self):
        return self.renderRect

    def getPosition(self):
        return list(self.position)

    def getPositionX(self):
        return self.position[0]

    def getPositionY(self):
        return self.position[1]

    def setPosition(self, x, y):
        self.position = [x, y]

    def setPositionX(self, x):
        self.position[0] = x

    def setPositionY(self, y):
        self.position[1] = y

    def movePosition(self, deltaX, deltaY):
        self.position[0] += deltaX
        self.position[1] += deltaY

    def setSize(self, width, height):
        self.size = [width, height]

    def getSize(self):
        return list(self.size)

    def getWidth(self):
        return self.getSize()[0]

    def getHeight(self):
        return self.getSize()[1]

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

    def draw(self, screen, offset=None):
        objectPosition = self.getPosition()
        if not offset is None:
            objectPosition[0] += offset[0]
            objectPosition[1] += offset[1]

        screen.blit(self.bitmap, objectPosition, self.getRenderRect())

    def render(self, screen, camera=None, offset=None):
        if self._isVisible:
            if offset is None:
                offset = [0, 0]

            if not camera is None:
                camera.transformWorldPosition(offset)

            self.draw(screen, offset)

            offset[0] += self.getPositionX()
            offset[1] += self.getPositionY()
            for child in self.children:
                child.render(screen, None, offset)

    def tick(self, delta):
        pass
