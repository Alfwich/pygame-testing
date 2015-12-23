import pygame
import StaticObject
from ..modules import fonts, colors

class Text(StaticObject.StaticObject):
    def __init__(self, text=None, font=None, color=colors.WHITE, backgroundColor=colors.TRANSPARENT):
        super(Text, self).__init__()
        self.text = str(text)
        self.font = font
        self.color = color
        self.backgroundColor = backgroundColor
        self._updateSurface()
        self.disableTick()

    def _updateSurface(self):
        self.setBitmap(fonts.renderTextSurface(self.text, self.font, self.color, self.backgroundColor))

    def setText(self, newText):
        self.text = str(newText)
        self._updateSurface()

    def setFont(self, newFont):
        self.font = newFont
        self._updateSurface()

    def setColor(self, newColor):
        self.color = newColor
        self._updateSurface()

    def setBackgroundColor(self, newBackgroundColor):
        self.backgroundColor = newBackgroundColor
        self._updateSurface()
