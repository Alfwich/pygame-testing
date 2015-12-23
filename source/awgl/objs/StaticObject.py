import pygame
from ..modules import events, colors
import GameObject

class StaticObject(GameObject.GameObject):

    def __init__(self):
        super(StaticObject, self).__init__()
        self.bitmap = None
        self.velocity = [0,0]
        self.renderRect = None

    def _updateRenderRect(self):
        self.renderRect = self.bitmap.get_rect()

    def setBitmap(self, surface):
        if not surface is None:
            self.setSize(surface.get_width(), surface.get_height())
            self.bitmap = surface
            self._updateRenderRect()

    def scaleBitmap(self, xScale, yScale):
        self.setBitmap(pygame.transform.scale(self.bitmap, (self.bitmap.get_width()*int(xScale), self.bitmap.get_height()*int(yScale))))

    def getBitmap(self):
        return self.bitmap

    def getRenderRect(self):
        return self.renderRect

    def setVelocity(self, velocityX, velocityY):
        self.velocity = [velocityX, velocityY]

    def setXVelocity(self, velocityX):
        self.velocity[0] = velocityX

    def setYVelocity(self, velocityY):
        self.velocity[1] = velocityY

    def addVelocity(self, deltaX, deltaY):
        self.velocity[0] += deltaX
        self.velocity[1] += deltaY

    def getVelocity(self):
        return list(self.velocity)

    def draw(self, screen, offset=None):
        objectPosition = self.getPosition()

        if not offset is None:
            objectPosition[0] += offset[0]
            objectPosition[1] += offset[1]

        screen.blit(self.bitmap, objectPosition, self.getRenderRect())
