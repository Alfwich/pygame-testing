import pygame

import events, renderer


try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    pass

IMAGE_LOAD_TEMPLATE = "data/image/%s"
_cachedImages = {}
_cachedOpenGLTextures = {}
_globalImageLoadList = []

def init():
    pygame.display.init()
    loadGlobalImageList()
    events.bindVideoChangeEvent(lambda e: clearOpenGLImageCache())

def clearOpenGLImageCache():
    global _cachedOpenGLTextures
    _cachedOpenGLTextures = {}

def unloadOpenGLImage(image):
    if image in _cachedOpenGLTextures:
        _cachedOpenGLTextures[image][1] -= 1
        if _cachedOpenGLTextures[image][1] == 0:
            _unloadOpenGLTexture(_cachedOpenGLTextures[image])
            del _cachedOpenGLTextures[image]

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
        image = _cachedImages[name] = pygame.image.load(IMAGE_LOAD_TEMPLATE % path)

    return _cachedImages[name]

def setImage(name, image):
    _cachedImages[name] = image

def loadOpenGLTexture(image):
    if image not in _cachedOpenGLTextures:
        textureData = pygame.image.tostring(image, "RGBA", 1)
        width = image.get_width()
        height = image.get_height()
        textureId = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textureId)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
        _cachedOpenGLTextures[image] = [textureId, 1]

    return _cachedOpenGLTextures[image][0]

def _unloadOpenGLTexture(textureId):
    if textureId and renderer.openGLIsEnabled():
        glDeleteTextures(textureId)

def getImage(name):
    if name in _cachedImages:
        return _cachedImages[name]
    else:
        print("Could not find image for name: '%s'")
