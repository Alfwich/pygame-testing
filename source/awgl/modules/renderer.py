import pygame, os
import display, colors

_openGLLoadFailure = True
_openGlEnabled = True
try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    print "Could not load OpenGL"
    _openGLLoadFailure = True
    _openGlEnabled = False

def init(size):
    if _openGlEnabled:
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity();
        gluOrtho2D(0, size[0], size[1], 0)
        glMatrixMode(GL_MODELVIEW)

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def openGLIsEnabled():
    return _openGlEnabled

def enableOpenGL():
    global _openGlEnabled
    if not _openGLLoadFailure and not _openGlEnabled:
        _openGlEnabled = True
        images.clearOpenGLImageCache()
        display.updateScreen()

def disableOpenGL():
    global _openGlEnabled
    if _openGlEnabled:
        _openGlEnabled = False
        display.updateScreen()

def clear():
    if _openGlEnabled:
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    else:
        display.getScreen().fill(colors.BLACK)

def update():
    return pygame.display.flip() if _openGlEnabled else pygame.display.update()

def _renderOpenGL(obj, pos):
    texture = obj.glTexture
    if texture:
        size = obj.size
        texturePos = obj.renderRect
        bitmapSize = map( float, obj.bitmap.get_size())
        normalizedTexturePos = (texturePos.x/bitmapSize[0], 1-texturePos.y/bitmapSize[1], texturePos.w/bitmapSize[0], texturePos.h/bitmapSize[1])
        glBindTexture(GL_TEXTURE_2D, texture)
        drawPoints = [
            (pos[0], pos[1]),
            (pos[0]+size[0], pos[1]),
            (pos[0]+size[0], pos[1]+size[1]),
            (pos[0], pos[1]+size[1])
        ]

        texPoints = [
            (normalizedTexturePos[0], normalizedTexturePos[1]),
            (normalizedTexturePos[0]+normalizedTexturePos[2], normalizedTexturePos[1]),
            (normalizedTexturePos[0]+normalizedTexturePos[2], normalizedTexturePos[1]-normalizedTexturePos[3]),
            (normalizedTexturePos[0], normalizedTexturePos[1]-normalizedTexturePos[3])
        ]

        glBegin(GL_QUADS)
        glColor3f(1.0, 1.0, 1.0)
        for tx, cr in zip(texPoints, drawPoints):
            glTexCoord2f(*tx); glVertex3f(cr[0], cr[1], 0.0)
        glEnd()
        return True
    return False

def _renderSoftware(obj, pos):
    screen = display.getScreen()
    if obj.bitmap:
        screen.blit(obj.bitmap, pos, obj.renderRect)
        return True
    return False

def renderObjectToScreen(obj, pos):
    return _renderOpenGL(obj, pos) if _openGlEnabled else _renderSoftware(obj, pos)
