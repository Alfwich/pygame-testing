import pygame, os, sys
import display, colors, images as awglImages

_openGLLoadFailure = False
_openGlEnabled = True

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    print "Could not load OpenGL"
    _openGLLoadFailure = True
    _openGlEnabled = False

def init(size):
    global _openGlEnabled, _openGLLoadFailure
    if _openGlEnabled:
        try:
            glClearColor(0.0, 0.0, 0.0, 1.0)
            glClear(GL_COLOR_BUFFER_BIT)

            glMatrixMode(GL_PROJECTION)
            glLoadIdentity();
            gluOrtho2D(0, size[0], size[1], 0)
            glMatrixMode(GL_MODELVIEW)

            glEnable(GL_TEXTURE_2D)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        except:
            print("Could not enable OpenGL. Reverting back to software mode.(%s)" % sys.exc_info()[0])
            _openGlEnabled = False
            _openGLLoadFailure = True
            display.updateScreen()

def openGLIsEnabled():
    return _openGlEnabled

def getRendererMode():
    return "opengl" if _openGlEnabled else "software"

def enableOpenGL():
    global _openGlEnabled, _openGLLoadFailure
    try:
        if not _openGLLoadFailure and not _openGlEnabled:
            if display.isFullscreen():
                display.disableFullscreen()
                _openGlEnabled = True
                display.enableFullscreen()
            else:
                _openGlEnabled = True
                display.updateScreen()
            awglImages.clearOpenGLImageCache()
    except:
        print("Could not enable OpenGL. Reverting back to software mode.(%s)" % sys.exc_info()[0])
        _openGlEnabled = False
        _openGLLoadFailure = True
        display.updateScreen()

def disableOpenGL():
    global _openGlEnabled
    if _openGlEnabled:
        if display.isFullscreen():
            display.disableFullscreen()
            _openGlEnabled = False
            display.enableFullscreen()
        else:
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
        tint = obj.tint
        colorOffset = 255
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
        glColor4f((tint.r+colorOffset)/255.0, (tint.g+colorOffset)/255.0, (tint.b+colorOffset)/255.0, tint.a/255.0)
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
