import pygame
from ..modules import events, colors
import GameObject

class StaticObject(GameObject.GameObject):

    def __init__(self):
        super(StaticObject, self).__init__()
        self._bitmap = None
        self.bitmap = None
        self.renderRect = None
        self.alpha = 255

    def _updateRenderRect(self):
        self.renderRect = self.bitmap.get_rect()

    def _updateAlpha(self):
        if not self._bitmap is None and self.alpha < 255:
            self.bitmap = self._bitmap.copy()
            self.bitmap.fill((255, 255, 255, self.alpha), None, pygame.BLEND_RGBA_MULT)

    def setBitmap(self, surface):
        if not surface is None:
            self.setSize(surface.get_width(), surface.get_height())
            self._bitmap = self.bitmap = surface
            self._updateAlpha()
            self._updateRenderRect()

    def setAlpha(self, newAlpha):
        self.alpha = newAlpha
        self._updateAlpha()

    def getAlpha(self):
        return self.alpha

    def scaleBitmap(self, xScale, yScale):
        self.setBitmap(pygame.transform.scale(self.bitmap, (self.bitmap.get_width()*int(xScale), self.bitmap.get_height()*int(yScale))))

    def getBitmap(self):
        return self.bitmap

    def getRenderRect(self):
        return self.renderRect

    def draw(self, screen, offset=None):
        objectPosition = self.getPosition()

        if not offset is None:
            objectPosition[0] += offset[0]
            objectPosition[1] += offset[1]

        screen.blit(self.bitmap, objectPosition, self.getRenderRect())
