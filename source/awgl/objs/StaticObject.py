import pygame
from ..modules import events, colors
import GameObject

class StaticObject(GameObject.GameObject):

    def __init__(self):
        super(StaticObject, self).__init__()
        self._cachedBitmap = None
        self._bitmap = None
        self._renderRect = None
        self._alpha = 255
        self._rotation = 0.0
        self._scale = [1, 1]

    def _updateRenderRect(self):
        self._renderRect = self._bitmap.get_rect()

    def _updateBitmap(self):
        if not self._cachedBitmap is None:
            self._bitmap = self._cachedBitmap.copy()
            if not self._scale[0] == 1 or not self._scale[1] == 1:
                self._bitmap = pygame.transform.scale(self._bitmap, (self.bitmap.get_width()*self._scale[0], self.bitmap.get_height()*self._scale[1]))
            if not self._rotation == 0.0:
                self._bitmap = pygame.transform.rotate(self._bitmap, self._rotation)
            if self._alpha < 255:
                self._bitmap.fill((255, 255, 255, self._alpha), None, pygame.BLEND_RGBA_MULT)


    @property
    def alpha(self, value):
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        self._alpha = value
        self._updateBitmap()

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = value
        self._updateBitmap

    @property
    def scale(self, newScale):
        self._scale[0] = int(newScale[0])
        self._scale[1] = int(newScale[1])

    @property
    def bitmap(self):
        return self._bitmap

    @bitmap.setter
    def bitmap(self, newSurface):
        if newSurface:
            self.size = (newSurface.get_width(), newSurface.get_height())
            self._cachedBitmap = self._bitmap = newSurface
            self._updateBitmap()
            self._updateRenderRect()

    @property
    def renderRect(self):
        return self._renderRect

    def draw(self, screen, offset=None):
        objectPosition = self.position

        if not offset is None:
            objectPosition[0] += offset[0]
            objectPosition[1] += offset[1]

        screen.blit(self.bitmap, objectPosition, self.renderRect)
