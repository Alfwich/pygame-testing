import pygame, random
from ..awgl.modules import *
from ..awgl.objs import *

class SOPowerUp(StaticObject.StaticObject):
    def __init__(self, gameState=None, spawnLocation=(0, 0)):
        super(SOPowerUp, self).__init__()
        self.setPosition(spawnLocation[0] * 32, spawnLocation[1] * 32)
        self.setGameState(gameState)
        self.enableCollision()
        self.setTag("powerup")
        powerupBitmap = pygame.Surface((10,10))
        powerupBitmap.fill(colors.BLUE)
        self.setBitmap(powerupBitmap)
        self.disableTick()
