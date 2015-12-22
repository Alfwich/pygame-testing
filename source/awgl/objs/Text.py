import pygame
import StaticObject
from ..modules import fonts, colors

class Text(StaticObject.StaticObject):
    def __init__(self, text, font=None, color=colors.WHITE):
        super(Text, self).__init__()
        self.setBitmap(fonts.renderTextSurface(str(text), font, color))
        self.disableTick()

    def updateText(self, newText, font=None, color=colors.WHITE):
        self.setBitmap(fonts.renderTextSurface(str(newText), font, color))
