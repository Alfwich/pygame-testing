import pygame, colors

fontObject = None

def init():
    global fontObject
    fontObject = pygame.font.Font('freesansbold.ttf', 32)

def renderTextSurface(text):
    if fontObject:
        return fontObject.render(text, True, colors.RED)
    else:
        print("Could not generate text: '%s' as a font could not be loaded" % text)
        return None
