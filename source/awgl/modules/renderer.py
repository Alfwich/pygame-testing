import pygame, os, sys
import display, colors, images as awglImages, events
from ..objs import GameObject

_openGLLoadFailure = False
_openGlEnabled = True
_skipRenderFrames = 0

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
    global _openGlEnabled, _openGLLoadFailure, _skipRenderFrames
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
            events.postVideoEvent()
            _skipRenderFrames = 2
    except:
        print("Could not enable OpenGL. Reverting back to software mode.(%s)" % sys.exc_info()[0])
        _openGlEnabled = False
        _openGLLoadFailure = True
        display.updateScreen()

def disableOpenGL():
    global _openGlEnabled, _skipRenderFrames
    if _openGlEnabled:
        if display.isFullscreen():
            display.disableFullscreen()
            _openGlEnabled = False
            display.enableFullscreen()
        else:
            _openGlEnabled = False
            display.updateScreen()
        events.postVideoEvent()
        _skipRenderFrames = 2

def clear():
    global _skipRenderFrames
    if _skipRenderFrames > 0:
        _skipRenderFrames -= 1
    if _openGlEnabled:
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    else:
        display.getScreen().fill(colors.BLACK)

def update():
    return pygame.display.flip() if _openGlEnabled else pygame.display.update()

def _renderOpenGL(obj, pos):
    texture = obj.glTexture
    if texture:
        glPushMatrix()
        size = obj.size
        scale = obj.scale
        size[0] *= scale[0]
        size[1] *= scale[1]
        texturePos = obj.renderRect
        bitmapSize = map( float, obj.bitmap.get_size())
        normalizedTexturePos = (texturePos.x/bitmapSize[0], 1-texturePos.y/bitmapSize[1], texturePos.w/bitmapSize[0], texturePos.h/bitmapSize[1])
        tint = obj.tint
        glBindTexture(GL_TEXTURE_2D, texture)
        drawPoints = [
            (-size[0]/2.0, -size[1]/2.0),
            (size[0]/2.0, -size[1]/2.0),
            (size[0]/2.0, size[1]/2.0),
            (-size[0]/2.0, size[1]/2.0)

        ]
        """
            (pos[0], pos[1]),
            (pos[0]+size[0], pos[1]),
            (pos[0]+size[0], pos[1]+size[1]),
            (pos[0], pos[1]+size[1])
        """

        texPoints = [
            (normalizedTexturePos[0], normalizedTexturePos[1]),
            (normalizedTexturePos[0]+normalizedTexturePos[2], normalizedTexturePos[1]),
            (normalizedTexturePos[0]+normalizedTexturePos[2], normalizedTexturePos[1]-normalizedTexturePos[3]),
            (normalizedTexturePos[0], normalizedTexturePos[1]-normalizedTexturePos[3])
        ]

        widthOffset = size[0] / (2.0*scale[0])
        heightOffset = size[1] / (2.0*scale[1])
        xTranslate = pos[0] + widthOffset
        yTranslate = pos[1] + heightOffset
        objAlignemnt = obj.alignment

        """
        if objAlignemnt[0] == GameObject.alignment.LEFT:
                xTranslate -= widthOffset
        elif objAlignemnt[0] == GameObject.alignment.RIGHT:
                xTranslate += widthOffset

        print objAlignemnt
        if objAlignemnt[1] == GameObject.alignment.BOTTOM:
                yTranslate -= heightOffset
        elif objAlignemnt[1] == GameObject.alignment.TOP:
                yTranslate += heightOffset
        """
        glTranslatef(xTranslate, yTranslate, 0.0)
        glRotatef(obj.rotation, 0.0, 0.0, 1.0)

        glBegin(GL_QUADS)
        glColor4f(tint.r/255.0, tint.g/255.0, tint.b/255.0, tint.a/255.0)
        for tx, cr in zip(texPoints, drawPoints):
            glTexCoord2f(*tx); glVertex3f(cr[0], cr[1], 0.0)
        glEnd()
        glPopMatrix()
        return True
    return False

def _renderSoftware(obj, pos):
    screen = display.getScreen()
    if obj.bitmap:
        screen.blit(obj.bitmap, pos, obj.renderRect)
        return True
    return False

def renderObjectToScreen(obj, pos):
    if _skipRenderFrames == 0:
        return _renderOpenGL(obj, pos) if _openGlEnabled else _renderSoftware(obj, pos)
