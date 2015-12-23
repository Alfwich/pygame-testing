import pygame
from ..modules import events

class alignment:
    TOP = LEFT = 0
    CENTER = 1
    BOTTOM = RIGHT = 2

class GameObject(object):
    def __init__(self):
        self._isVisible = True
        self._isValid = True
        self._canTick = False
        self._boundEvents = []
        self.position = [0, 0]
        self.size = [0, 0]
        self.children = []
        self.alignment = [alignment.CENTER, alignment.CENTER]
        self.enableTick()

    def _alignAxis(self, axisValue, dimSize, align):
        if align == alignment.CENTER:
            return axisValue - dimSize/2
        elif align == alignment.BOTTOM:
            return axisValue - dimSize
        else:
            return axisValue

    def _alignPosition(self, position):
        size = self.getSize()
        newPosition = [position[0], position[1]]
        for axis, align in enumerate(self.alignment):
            newPosition[axis] = self._alignAxis(newPosition[axis], size[axis], align)
        return newPosition

    def setAlignment(self, alignX, alignY):
        self.alignment = [alignX, alignY]

    def setAlignmentX(self, alignX):
        self.alignment[0] = alignX

    def setAlignmentY(self, alignY):
        self.alignment[1] = alignY

    def getPosition(self):
        return map(int, self.position)

    def getPositionX(self):
        return self.getPosition()[0]

    def getPositionY(self):
        return self.getPosition()[1]

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

    def render(self, screen, camera=None, offset=None):
        if self.isVisible():
            if offset is None:
                offset = [0, 0]

            if not camera is None:
                camera.transformWorldPosition(offset)

            if hasattr(self, "draw"):
                alignedOffset = self._alignPosition(offset)
                self.draw(screen, alignedOffset)

            offset[0] += self.getPositionX()
            offset[1] += self.getPositionY()
            for child in self.children:
                child.render(screen, None, list(offset))

    def tick(self, delta):
        pass
