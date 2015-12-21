import pygame

IMAGE_LOAD_TEMPLATE = "src/image/%s"
_loadedImages = {}
_globalImageLoadList = []

def init():
    pygame.init()

def addToGlobalLoadList(newList):
    for asset in newList:
        _globalImageLoadList.append(asset)

def loadGlobalImageList():
    loadImageList(_globalImageLoadList)

def loadImageList(imageList):
    for asset in imageList:
        loadImage(*asset)

def loadImage(name, path):
    if not name in _loadedImages:
        _loadedImages[name] = pygame.image.load(IMAGE_LOAD_TEMPLATE % path)

    return _loadedImages[name]

def getImage(name):
    if name in _loadedImages:
        return _loadedImages[name]
    else:
        print("Could not find image for name: '%s'")
