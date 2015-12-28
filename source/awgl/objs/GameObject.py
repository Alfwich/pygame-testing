import pygame
from ..modules import events

class alignment:
    TOP = LEFT = 0
    CENTER = 1
    BOTTOM = RIGHT = 2
    LEFT_TOP = (LEFT, TOP)
    CENTER_TOP = (CENTER, TOP)
    RIGHT_TOP = (RIGHT, TOP)
    LEFT_CENTER = (LEFT, CENTER)
    MIDDLE = CENTER_CENTER = (CENTER, CENTER)
    RIGHT_CENTER = (RIGHT, CENTER)
    LEFT_BOTTOM = (LEFT, BOTTOM)
    CENTER_BOTTOM = (CENTER, BOTTOM)
    RIGHT_BOTTOM = (RIGHT, BOTTOM)


class GameObject(object):
    def __init__(self):
        self._isVisible = True
        self._isValid = True
        self._canTick = False
        self._priority = 10
        self._canCollide = False
        self._boundEvents = []
        self._position = [0, 0]
        self._size = [0, 0]
        self.rect = pygame.Rect(0,0,0,0)
        self._gameState = None
        self.tags = {}
        self._parent = None
        self._children = []
        self._alignment = list(alignment.MIDDLE)

    def _alignAxis(self, axisValue, dimSize, align):
        if align == alignment.CENTER:
            return axisValue - dimSize/2
        elif align == alignment.BOTTOM:
            return axisValue - dimSize
        else:
            return axisValue

    def _alignPosition(self, position):
        size = self.size
        newPosition = [position[0], position[1]]
        for axis, align in enumerate(self._alignment):
            newPosition[axis] = self._alignAxis(newPosition[axis], size[axis], align)
        return newPosition

    def setTag(self, tag, value=True):
        self.tags[tag] = value

    def getTag(self, tag):
        return self.tags[tag] if tag in self.tags else None

    def removeTag(self, tag):
        if tag in self.tags:
            del self.tags[tag]

    def hasTag(self, tag):
        return tag in self.tags

    @property
    def gameState(self):
        return self._gameState

    @gameState.setter
    def gameState(self, newState):
        if self._gameState is None:
            self._gameState = newState

    @property
    def gameWorld(self):
        gameState = self.gameState
        if gameState:
            return gameState.world

    @property
    def canCollide(self):
        return self._canCollide

    @canCollide.setter
    def canCollide(self, newValue):
        if self.gameState and not newValue is self._canCollide:
            self._canCollide = newValue
            if newValue:
                self.gameState.registerCollidableObject(self)
            else:
                self.gameState.deregisterCollidableObject(self)

    @property
    def alignment(self):
        return self._alignment

    @alignment.setter
    def alignment(self, newAlignment):
        self._alignment[0] = newAlignment[0]
        self._alignment[1] = newAlignment[1]

    @property
    def alignmentX(self, alignX):
        return self._alignment[0]

    @alignment.setter
    def alignmentX(self, alignX):
        self._alignment[0] = alignX

    @property
    def alignmentY(self, alignY):
        return self._alignment[1]

    @alignment.setter
    def alignmentY(self, alignY):
        self._alignment[1] = alignY

    @property
    def position(self):
        return [int(self._position[0]), int(self._position[1])]

    @property
    def rawPosition(self):
        return list(self._position)

    @property
    def positionX(self):
        return self._position[0]

    @property
    def positionY(self):
        return self._position[1]

    @position.setter
    def position(self, newPosition):
        self._position[0] = newPosition[0]
        self._position[1] = newPosition[1]

    @positionX.setter
    def positionX(self, x):
        self._position[0] = x

    @positionY.setter
    def positionY(self, y):
        self._position[1] = y

    def movePosition(self, deltaX, deltaY):
        self._position[0] += deltaX
        self._position[1] += deltaY

    def movePositionX(self, deltaX):
        self._position[0] += deltaX

    def movePositionY(self, deltaY):
        self._position[1] += deltaY

    @property
    def size(self):
        return [self._size[0], self._size[1]]

    @size.setter
    def size(self, newSize):
        self._size[0] = newSize[0]
        self._size[1] = newSize[1]

    def getRect(self):
        position = self._alignPosition(self.position)
        size = self.size
        return pygame.Rect(position[0], position[1], size[0], size[1])

    def getRawRect(self):
        rect = self.getRect()
        return (rect.x, rect.y, rect.w, rect.h)

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]

    def addEvents(self, eventIds):
        if not isinstance(eventIds, list):
            eventIds = [eventIds]

        for eventId in eventIds:
            self._boundEvents.append(eventId)

    @property
    def visible(self):
        return self._isVisible

    @visible.setter
    def visible(self, visibility):
        self._isVisible = visibility

    def addEvents(self, eventIds):
        if not isinstance(eventIds, list):
            eventIds = [eventIds]

        for eventId in eventIds:
            self._boundEvents.append(eventId)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, newParent):
        self._parent = newParent

    def addChild(self, child):
        child.parent = self
        self._children.append(child)

    def removeChild(self, child):
        if child in self._children:
            self._children.remove(child)

    def disable(self):
        self.disabled = True

    @property
    def disabled(self):
        return not self._isValid

    @disabled.setter
    def disabled(self, newValue):
        if self._isValid and newValue:
            self._isValid = False
            for eventId in self._boundEvents:
                events.unbindEvent(eventId)
            self._boundEvents = []
            self.visible = False
            self.canTick = False
            if self._parent:
                self._parent.removeChild(self)
            self._parent = None

            for child in self._children:
                child.disable()
            self._children = []

            if self.gameState:
                self.gameState.deregisterCollidableObject(self)

    @property
    def canTick(self):
        return self._canTick

    @canTick.setter
    def canTick(self, newValue):
        if not newValue is self._canTick:
            self._canTick = newValue
            if newValue:
                events.registerTickableObject(self, self._priority)
            else:
                events.deregisterTickableObject(self)

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, newValue):
        if not self._priority == newValue:
            self._priority = newValue
            if self.canTick:
                events.deregisterTickableObject(self)
                events.registerTickableObject(self, self._priority)


    def render(self, screen, camera=None, offset=None):
        if self.visible:
            if offset is None:
                offset = [0, 0]

            if not camera is None:
                camera.transformWorldPosition(offset)

            if hasattr(self, "draw"):
                alignedOffset = self._alignPosition(offset)
                self.draw(screen, alignedOffset)

            offset[0] += self.positionX
            offset[1] += self.positionY
            for child in self._children:
                child.render(screen, None, list(offset))

    def hasCollided(self, other):
        return False

    def tick(self, delta):
        pass

    def bindEvents(self):
        pass

    def begin(self):
        pass
