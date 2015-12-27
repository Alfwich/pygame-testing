import pygame, random
from ..awgl.modules import *
from ..awgl.objs import *
import AOPlayerCharacter

class SOPowerUp(StaticObject.StaticObject):
    def __init__(self, gameState=None, spawnLocation=(0, 0)):
        super(SOPowerUp, self).__init__()
        self.setPosition(spawnLocation[0] * 32 + 16, spawnLocation[1] * 32 + 16)
        self.setGameState(gameState)
        self.enableCollision()
        self.setTag("powerup")
        powerupBitmap = pygame.Surface((10,10))
        powerupBitmap.fill(colors.BLUE)
        self.setBitmap(powerupBitmap)
        self.disableTick()

    def hasCollided(self, other):
        if isinstance(other, AOPlayerCharacter.AOPlayerCharacter):
            other.walkingSpeed *= 1.1
