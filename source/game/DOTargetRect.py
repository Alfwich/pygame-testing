import pygame, pygame.gfxdraw, random
from ..awgl.modules import colors, draw, math
from ..awgl.objs import *

def drawBox(obj, screen, offset):
    boxPosition = obj.position
    if offset:
        boxPosition[0] += offset[0]
        boxPosition[1] += offset[1]

    draw.box(screen, boxPosition, (boxPosition[0]+obj.width, boxPosition[1]+obj.height), obj.color, 2)

class DOTargetRect(DrawableObject.DrawableObject):
    def __init__(self, **configuration):
        super(DOTargetRect, self).__init__()
        self._color = pygame.Color(255, 0, 0, 255)
        self._colorAlpha = 255.0
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
        self._colorAlpha = 255.0
        self.canTick = self.visible = True

    def tick(self, delta):
        super(DOTargetRect, self).tick(delta)
        if self._target and self._colorAlpha > 0.0:
            self.position = self._target.position
            self._colorAlpha -= 128.0 * delta
            self._color.a = math.clamp(0, 255, int(self._colorAlpha))
        else:
            self.visible = self.canTick = False
