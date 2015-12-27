import pygame
import StaticObject
from ..modules import fonts, colors

class Text(StaticObject.StaticObject):
    def __init__(self, text=None, font=None, color=colors.WHITE, backgroundColor=colors.TRANSPARENT):
        super(Text, self).__init__()
        self._text = str(text)
        self._font = font
        self._color = color
        self._backgroundColor = backgroundColor
        self._updateSurface()
        self.canTick = False

    def _updateSurface(self):
        self.bitmap = fonts.renderTextSurface(self._text, self._font, self._color, self._backgroundColor)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, newText):
        self._text = str(newText)
        self._updateSurface()

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, newFont):
        self._font = newFont
        self._updateSurface()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, newColor):
        self._color = newColor
        self._updateSurface()

    @property
    def backgroundColor(self):
        return self._backgroundColor

    @backgroundColor.setter
    def backgroundColor(self, newBackgroundColor):
        self._backgroundColor = newBackgroundColor
        self._updateSurface()
