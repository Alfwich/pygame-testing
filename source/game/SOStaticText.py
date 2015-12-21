import pygame
from ..awgl.modules import *
from ..awgl.objs import *

class SOStaticText(StaticObject.StaticObject):
    def __init__(self, text):
        super(SOStaticText, self).__init__()
        self.setBitmap(fonts.renderTextSurface(text))

    def updateText(self, newText):
        self.setBitmap(fonts.renderTextSurface(newText))
