from ..modules import display, math
from ..objs import GameObject

class Camera(GameObject.GameObject):
    def __init__(self):
        super(Camera, self).__init__()
        self._focus = None
        self._transitionTime = 0.0
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
    def focus(self):
        return self._focus

    @focus.setter
    def focus(self, newFocus):
        self.canTick = True
        self._transitionTime = 0.0
        self._startPosition = self.position
        self._focus = newFocus

    def moveOffset(self, deltaX, deltaY):
        self.positionX += deltaX
        self.positionY += deltaY

    def centerOnObject(self, obj):
        objectPosition = obj.position
        screenSize = display.getScreenSize()
        desired = [int(screenSize[0]/2 - objectPosition[0]), int(screenSize[1]/2 - objectPosition[1])]
        if self._transitionTime < 1.0:
            self.position = math.vectorLerp(self._startPosition, desired, self._transitionTime)
        else:
            self.position = desired

    def tick(self, delta):
        super(Camera, self).tick(delta)
        if self._focus:
            if self._transitionTime < 1.0:
                self._transitionTime += delta
            self.centerOnObject(self._focus)

        else:
            self.canTick = False
