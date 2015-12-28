import pygame, random
from ..awgl.modules import *
from ..awgl.objs import *

class SOScreenFader(StaticObject.StaticObject):
    def __init__(self, **configuration):
        super(SOScreenFader, self).__init__()
        self._fadeDirection = 0
        self._ignoreFrames = 0
        self.alpha = 255
        self.fadeSpeed = configuration.get("fadeSpeed", 30)
        self.position = map(lambda c: c/2, display.getScreenSize())
        self.canTick = False
        self.screenText = Text.Text()
        self.screenText.alignment = GameObject.alignment.RIGHT_BOTTOM
        self.children.append(self.screenText)
        self._updateScreenBitmap()
        self.addEvents(events.bindVideoChangeEvent(self._updateScreenBitmap))

    def _updateScreenBitmap(self, event=None):
        screenBitmap = pygame.Surface(display.getScreenSize())
        screenBitmap.fill(colors.BLACK)
        self.bitmap = screenBitmap
        self.position = map(lambda c: c/2, display.getScreenSize())
        self.screenText.position = map(lambda c: c-10, self.position)

    def fadeOut(self):
        self.alpha = 255
        self.screenText.text = ""
        self._fadeDirection = -1
        self._ignoreFrames = 2
        self.canTick = True

    def fadeIn(self, text=""):
        self.alpha = 0
        self.screenText.text = "Loading: %s" % text
        self._fadeDirection = 1
        self._ignoreFrames = 2
        self.canTick = True

    def tick(self, delta):
        super(SOScreenFader, self).tick(delta)
        if self._ignoreFrames <= 0:
            self.alpha += delta * self.fadeSpeed * self._fadeDirection
            if self.alpha <= 0 or self.alpha >= 255:
                self._fadeDirection = 0
                self.canTick = False
        else:
            self._ignoreFrames -= 1
