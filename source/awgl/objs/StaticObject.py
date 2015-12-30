import pygame
from ..modules import events, colors, renderer, images, math
import GameObject

class StaticObject(GameObject.GameObject):

    def __init__(self):
        super(StaticObject, self).__init__()
        self._cachedBitmap = None
        self._texture = None
        self._bitmap = None
        self._bitmapIsDirty = False
        self._renderRect = None
        self._rotation = 0.0
        self._scale = [1, 1]
        self._tint = pygame.Color("#ffffffff")

    def _updateRenderRect(self):
        self._renderRect = self._bitmap.get_rect()

    def _updateBitmap(self):
        if self._bitmap:
            if not self._cachedBitmap is None and self.visible:
                self._bitmap = self._cachedBitmap.copy()
                if not self._tint == colors.DEFAULT_TINT:
                    self._bitmap.fill(self._tint, None, pygame.BLEND_RGBA_MULT)
                if not self._scale[0] == 1 or not self._scale[1] == 1:
                    self._bitmap = pygame.transform.scale(self._bitmap, (self.bitmap.get_width()*self._scale[0], self.bitmap.get_height()*self._scale[1]))
                if not self._rotation == 0.0:
                    self._bitmap = pygame.transform.rotate(self._bitmap, self._rotation)
            images.unloadOpenGLImage(self._bitmap)
            self._bitmapIsDirty = False


    @property
    def glTexture(self):
        openGlTextureId = images.loadOpenGLTexture(self._bitmap)
        return openGlTextureId

    @property
    def tint(self):
        return self._tint

    @tint.setter
    def tint(self, newTint):
        if not isinstance(newTint, pygame.Color):
            newTint = pygame.Color(*newTint)
        self._tint.r = newTint.r
        self._tint.g = newTint.g
        self._tint.b = newTint.b
        self._bitmapIsDirty = True
        if not renderer.openGLIsEnabled():
            self._updateBitmap()

    @property
    def alpha(self):
        return self._tint.a

    @alpha.setter
    def alpha(self, value):
        newAlphaValue = int(sorted([0.0, value, 255.0])[1])
        if not newAlphaValue == self._tint.a:
            self._tint.a = newAlphaValue
            if self._tint.a <= 0:
                self.visible = False
            else:
                self.visible = True

            self._bitmapIsDirty = True
            if not renderer.openGLIsEnabled():
                self._updateBitmap()

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = value
        self._bitmapIsDirty = True
        self._updateBitmap()

    @property
    def scale(self):
        return list(self._scale)

    @scale.setter
    def scale(self, newScale):
        self._scale[0] = int(newScale[0])
        self._scale[1] = int(newScale[1])
        self._bitmapIsDirty = True
        self._updateBitmap()

    @property
    def bitmap(self):
        if self._bitmapIsDirty:
            self._updateBitmap()
        return self._bitmap

    @bitmap.setter
    def bitmap(self, newSurface):
        if newSurface:
            self._cachedBitmap = self._bitmap = newSurface.convert_alpha()
            self._updateBitmap()
            self.size = (self._bitmap.get_width(), self._bitmap.get_height())
            self._updateRenderRect()

    @property
    def renderRect(self):
        return self._renderRect

    def draw(self, screen, offset=None):
        objectPosition = self.position

        if not offset is None:
            objectPosition[0] += offset[0]
            objectPosition[1] += offset[1]

        renderer.renderObjectToScreen(self, objectPosition)
