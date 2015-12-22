import pygame
import StaticObject
from ..modules import fonts

class Text(StaticObject.StaticObject):
    def __init__(self, text):
        super(Text, self).__init__()
        self.setBitmap(fonts.renderTextSurface(str(text)))
        self.disableTick()

    def updateText(self, newText):
        self.setBitmap(fonts.renderTextSurface(str(newText)))
