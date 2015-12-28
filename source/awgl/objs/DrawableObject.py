import GameObject
from ..modules import *

class DrawableObject(GameObject.GameObject):
    def __init__(self):
        super(DrawableObject, self).__init__()
        self._drawFunction = None

    @property
    def drawFunction(self):
        return self._drawFunction

    @drawFunction.setter
    def drawFunction(self, newFunction):
        self._drawFunction = newFunction

    def draw(self, screen, offset=None):
        if not self._drawFunction is None:
            self._drawFunction(self, screen, offset)
