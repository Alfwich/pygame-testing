import pygame, random
from ..awgl.modules import draw, events, display, math
from ..awgl.objs import DrawableObject, Text, GameObject

def drawScreenFader(obj, screen, offset):
    draw.box(screen, (0, 0), display.getScreenSize(), pygame.Color(0, 0, 0, obj.alpha))

class DOScreenFader(DrawableObject.DrawableObject):
    def __init__(self, **configuration):
        super(DOScreenFader, self).__init__()
        self._fadeDirection = 0
        self._ignoreFrames = 0
        self._alpha = 255
        self.fadeSpeed = configuration.get("fadeSpeed", 30)
        self.screenText = Text.Text()
        self.screenText.alignment = GameObject.alignment.BOTTOM_RIGHT
        self.addChild(self.screenText)
        self._updateScreenBitmap()
        self.addEvents(events.bindVideoChangeEvent(self._updateScreenBitmap))
        self.drawFunction = drawScreenFader

    def _updateScreenBitmap(self, event=None):
        self.position = display.getScreenSize()
        self.screenText.position = (-10, -10)

    @property
    def isAnimating(self):
        return not self.alpha == 0

    @property
    def estimatedFadeTime(self):
        return 1000 * (255 / float(self.fadeSpeed)) + 200

    @property
    def alpha(self):
        return math.clamp(0, 255, int(self._alpha))

    @alpha.setter
    def alpha(self, newAlpha):
        self._alpha = newAlpha

    def fadeOut(self):
        self.alpha = 255
        self.screenText.text = ""
        self._fadeDirection = -1
        self._ignoreFrames = 2
        self.canTick = True

    def fadeIn(self, text=""):
        self.alpha = 0
        self.visible = True
        self.screenText.text = "Loading: %s" % text
        self._fadeDirection = 1
        self._ignoreFrames = 2
        self.canTick = True

    def tick(self, delta):
        super(DOScreenFader, self).tick(delta)
        if self._ignoreFrames <= 0:
            self.alpha += delta * self.fadeSpeed * self._fadeDirection
            if self.alpha <= 0 or self.alpha >= 255:
                self._fadeDirection = 0
                if self.alpha <= 0:
                    self.visible = False
                self.canTick = False
        else:
            self._ignoreFrames -= 1
