import pygame, random
from ..awgl.modules import clock, display, colors, fonts, renderer
from ..awgl.objs import Text, GameObject

fonts.addToGlobalLoadList([
    ("console", "cour.ttf", 24)
])

class TInfoText(Text.Text):
    def __init__(self):
        super(TInfoText, self).__init__(self._generateText())
        self._displayTime = 0.0
        self.font = fonts.getFont("console")
        self.backgroundColor = colors.BLACK
        self.alignment = GameObject.alignment.TOP_LEFT
        self.canTick = True

    def _generateText(self):
        return "res: %s, fps: %.2f(%s)" % (display.getScreenSize(), clock.getFPS(), renderer.getRendererMode())

    def tick(self, delta):
        self._displayTime += delta
        if self._displayTime > 0.25:
            self._displayTime -= 0.25
            self.text = self._generateText()
