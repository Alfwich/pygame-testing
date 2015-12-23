import pygame, random
from ..awgl.modules import clock, display, colors, fonts
from ..awgl.objs import Text, GameObject

fonts.addToGlobalLoadList([
    ("console", "cour.ttf", 24)
])

class TInfoText(Text.Text):
    def __init__(self):
        super(TInfoText, self).__init__(self._generateText())
        self.setFont(fonts.getFont("console"))
        self.setBackgroundColor(colors.BLACK)
        self.setAlignment(GameObject.alignment.LEFT, GameObject.alignment.TOP)
        self.enableTick()

    def _generateText(self):
        return "res: %s, fps: %.2f" % (display.getScreenSize(), clock.getFPS())

    def tick(self, delta):
        self.setText(self._generateText())
