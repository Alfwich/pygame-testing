import pygame, random
from ..awgl.modules import *
from ..awgl.objs import *
import AOPlayerCharacter

class SOPowerUp(StaticObject.StaticObject):
    def __init__(self, **configuration):
        super(SOPowerUp, self).__init__()
        self.setTag("powerup")
        powerupBitmap = pygame.Surface((10,10))
        powerupBitmap.fill(colors.BLUE)
        self.bitmap = powerupBitmap

    def begin(self):
        super(SOPowerUp, self).begin()
        self.canCollide = True

    def hasCollided(self, other):
        if isinstance(other, AOPlayerCharacter.AOPlayerCharacter):
            other.walkingSpeed *= 1.1
            other.currentSpeed *= 1.1
            self.disable()
            return True
