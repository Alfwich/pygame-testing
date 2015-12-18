import pygame, random

_loadedColors = {}
BLACK = "black"
WHITE = "white"
RED = "red"
GREEN = "green"
BLUE = "blue"
DEFAULT = WHITE


def init():
    loadColor(WHITE, 255, 255, 255)
    loadColor(BLACK, 0, 0, 0)
    loadColor(RED, 255, 0, 0)
    loadColor(GREEN, 0, 255, 0)
    loadColor(BLUE, 0, 0, 255)

def loadColor(colorName, r, g, b, a=255):
    _loadedColors[colorName] = pygame.Color(r, g, b, a)

def getColor(colorName):
    if colorName in _loadedColors:
        return _loadedColors[colorName]
    else:
        print("Could not retrive color: '%s'" % (colorName))
        return _loadedColors[DEFAULT]

def randomColor():
    return (random.randint(0,255), random.randint(0,255), random.randint(0,255))
