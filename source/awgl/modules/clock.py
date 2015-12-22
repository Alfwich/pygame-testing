import pygame
import display

_gameClock = None
_globalTimeModifier = 1.0
_isPaused = False

def init():
    pygame.display.init()
    global _gameClock
    _gameClock = pygame.time.Clock()

def getFPS():
    return _gameClock.get_fps()

def setGlobalTimeModifier(newModifier):
    global _globalTimeModifier
    _globalTimeModifier = newModifier

def pause():
    global _isPaused
    _isPaused = True

def unpause():
    global _isPaused
    _isPaused = False

def tick():
    return 0.0 if _isPaused else (_gameClock.tick(display.getDesiredFPS()) * _globalTimeModifier)/1000.0
