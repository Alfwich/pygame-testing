import pygame, pygame.gfxdraw
import display, renderer, colors

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    pass

def _rectFromTopLeftBottomRight(topLeft, bottomRight):
    return (topLeft[0], topLeft[1], bottomRight[0]-topLeft[0], bottomRight[1]-topLeft[1])

def _lineSoftware(surface, start, end, color, width):
    pygame.draw.line(surface, color, start, end, width)

def _lineOpenGL(start, end, color, width):
    glLineWidth(width)
    glBindTexture(GL_TEXTURE_2D, 0)
    glBegin(GL_LINES)
    glColor4f(color.r/255.0, color.g/255.0, color.b/255.0, color.a/255.0)
    glVertex2f(*start); glVertex2f(*end)
    glEnd()

def line(surface, start, end, color=colors.WHITE, width=1):
    _lineOpenGL(start, end, color, width) if renderer.openGLIsEnabled() else _lineSoftware(surface, start, end, color, width)

def _boxSoftware(surface, topLeft, bottomRight, color, width):
    if width > 0:
        boxWidth = bottomRight[0]-topLeft[0]
        boxHeight = bottomRight[1]-topLeft[1]
        # Draws the box in Top, Right, Bottom, Left order
        pygame.gfxdraw.box(surface, (topLeft[0], topLeft[1], boxWidth, width), color)
        pygame.gfxdraw.box(surface, (bottomRight[0], topLeft[1], width, boxHeight), color)
        pygame.gfxdraw.box(surface, (topLeft[0], bottomRight[1], boxWidth, width), color)
        pygame.gfxdraw.box(surface, (topLeft[0], topLeft[1], width, boxHeight), color)

        #pygame.draw.rect(surface, color, _rectFromTopLeftBottomRight(topLeft, bottomRight), width)
    else:
        surface.fill(color, _rectFromTopLeftBottomRight(topLeft, bottomRight))

def _boxOpenGL(topLeft, bottomRight, color, width):
    glBindTexture(GL_TEXTURE_2D, 0)
    if width > 0:
        glLineWidth(width)
        glBegin(GL_LINES)
        glColor4f(color.r/255.0, color.g/255.0, color.b/255.0, color.a/255.0)
        glVertex2f(*topLeft); glVertex2f(bottomRight[0], topLeft[1])
        glVertex2f(bottomRight[0], topLeft[1]); glVertex2f(*bottomRight);
        glVertex2f(*bottomRight); glVertex2f(topLeft[0], bottomRight[1])
        glVertex2f(topLeft[0], bottomRight[1]); glVertex2f(*topLeft)
        glEnd()
    else:
        glBegin(GL_QUADS)
        glColor4f(color.r/255.0, color.g/255.0, color.b/255.0, color.a/255.0)
        glVertex2f(*topLeft); glVertex2f(bottomRight[0], topLeft[1])
        glVertex2f(*bottomRight); glVertex2f(topLeft[0], bottomRight[1])
        glEnd()

def box(surface, topLeft, bottomRight, color=colors.WHITE, width=0):
    _boxOpenGL(topLeft, bottomRight, color, width) if renderer.openGLIsEnabled() else _boxSoftware(surface, topLeft, bottomRight, color, width)
