import pygame

import events

from OpenGL.GL import *
from OpenGL.GLU import *

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
    if id(image) in _cachedOpenGLTextures:
        unloadOpenGLTexture(_cachedOpenGLTextures[id(image)])
        del _cachedOpenGLTextures[id(image)]

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

def loadOpenGLTexture(image):
    if id(image) not in _cachedOpenGLTextures:
        textureData = pygame.image.tostring(image, "RGBA", 1)
        width = image.get_width()
        height = image.get_height()
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
        _cachedOpenGLTextures[id(image)] = texture
    return _cachedOpenGLTextures[id(image)]

def unloadOpenGLTexture(textureId):
    glDeleteTextures(textureId)

def getImage(name):
    if name in _cachedImages:
        return _cachedImages[name]
    else:
        print("Could not find image for name: '%s'")
