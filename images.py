import pygame

_loadedImages = {}

def loadImage(name, path):
    if not name in _loadedImages:
        _loadedImages[name] = pygame.image.load(path)

    return _loadedImages[name]

def getImage(name):
    return _loadedImages[name] if name in _loadedImages else None
