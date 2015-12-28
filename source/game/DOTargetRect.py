import pygame, pygame.gfxdraw, random, math
from ..awgl.modules import colors
from ..awgl.objs import *

def drawBox(obj, screen, offset):
    boxPosition = obj.position
    if offset:
        boxPosition[0] += offset[0]
        boxPosition[1] += offset[1]

    pygame.gfxdraw.rectangle(screen, pygame.Rect(boxPosition[0], boxPosition[1], obj.width, obj.height), obj.color)

class DOTargetRect(DrawableObject.DrawableObject):
    def __init__(self, **configuration):
        super(DOTargetRect, self).__init__()
        self._color = colors.RED
        self._target = None
        self.size = configuration.get("size", (100, 100))
        self.drawFunction = drawBox

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, newColor):
        if not isinstance(newColor, pygame.Color):
            newColor = pygame.Color(*newColor)
        self._color.r = newColor.r
        self._color.g = newColor.g
        self._color.b = newColor.b

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, newTarget):
        self._target = newTarget
        self.size = newTarget.size
        self.alignment = newTarget.alignment
        self._color.a = 255
        self.canTick = True

    def tick(self, delta):
        super(DOTargetRect, self).tick(delta)
        if self._target and self._color.a > 0:
            self.position = self._target.position
            self._color.a -= 1
        else:
            self.canTick = False
