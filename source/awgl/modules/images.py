import pygame

IMAGE_LOAD_TEMPLATE = "data/image/%s"
_cachedImages = {}
_globalImageLoadList = []

def init():
    pygame.display.init()
    loadGlobalImageList()

def addToGlobalLoadList(newList):
    for asset in newList:
        _globalImageLoadList.append(asset)

def loadGlobalImageList():
    loadImageList(_globalImageLoadList)

def loadImageList(imageList):
    for asset in imageList:
        loadImage(*asset)

def loadImage(name, path):
    if not name in _cachedImages:
        _cachedImages[name] = pygame.image.load(IMAGE_LOAD_TEMPLATE % path)

    return _cachedImages[name]

def getImage(name):
    if name in _cachedImages:
        return _cachedImages[name]
    else:
        print("Could not find image for name: '%s'")
