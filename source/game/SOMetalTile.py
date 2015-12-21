import pygame, random
from ..awgl.modules import *
from ..awgl.objs import *

images.addToGlobalLoadList([
    ("metal-tile-texture", "metal.png")
])

class SOMetalTile(StaticObject.StaticObject):
    def __init__(self, tileWidth, tileHeight):
        super(SOMetalTile, self).__init__()
        self.setBitmap(images.getImage("metal-tile-texture"))
        self.setSize(tileWidth, tileHeight)
        self._setupRenderRect(tileWidth, tileHeight)
        #self.disableTick()

    def _setupRenderRect(self, tileWidth, tileHeight):
        bitmapRect = self.bitmap.get_rect()
        randomBlockX = random.randint(0, bitmapRect.w-tileWidth)
        randomBlockY = random.randint(0, bitmapRect.h-tileHeight)
        self.renderRect = pygame.Rect(randomBlockX, randomBlockY, tileWidth, tileHeight)

    def getRenderRect(self):
        return self.renderRect

    def tick(self, delta):
        self.addPosition(random.randint(-1,1)*delta*20, random.randint(-1,1)*delta*20)
