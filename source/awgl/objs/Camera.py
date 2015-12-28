from ..modules import display, math
from ..objs import GameObject

class Camera(GameObject.GameObject):
    def __init__(self):
        super(Camera, self).__init__()
        self._target = None
        self._transitionTime = 1.0
        self._transitionDuration = 1.0
        self._startPosition = [0, 0]
        self.canTick = False

    def transformWorldPosition(self, position):
        position[0] += self.positionX
        position[1] += self.positionY

    def transformScreenPosition(self, position):
        position[0] -= self.positionX
        position[1] -= self.positionY

    def transformRectWorldPosition(self, rect):
        rect.x += self.positionX
        rect.y += self.positionY

    def transformRectScreenPosition(self, rect):
        rect.x -= self.positionX
        rect.y -= self.positionY

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, newTarget):
        self.canTick = True
        self._target = newTarget
        self._transitionTime = 0.0
        self._startPosition = self.position

    def forceFinishAnimation(self):
        self._transitionTime = 1.0

    @property
    def transitionDuration(self):
        return self._transitionDuration

    @transitionDuration.setter
    def transitionDuration(self, newValue):
        self._transitionDuration = newValue

    def moveOffset(self, deltaX, deltaY):
        self.positionX += deltaX
        self.positionY += deltaY

    def centerOnObject(self, obj):
        objectPosition = obj.position
        screenSize = display.getScreenSize()
        desired = [int(screenSize[0]/2 - objectPosition[0]), int(screenSize[1]/2 - objectPosition[1])]
        if self._transitionTime < self._transitionDuration:
            self.position = math.vectorLerp(self._startPosition, desired, self._transitionTime/self._transitionDuration)
        else:
            self.position = desired

    def tick(self, delta):
        super(Camera, self).tick(delta)
        if self._target:
            if self._transitionTime < self._transitionDuration:
                self._transitionTime += delta
            self.centerOnObject(self._target)
        else:
            self.canTick = False
