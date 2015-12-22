import pygame, colors

FONT_LOAD_TEMPLATE = "data/font/%s"
DEFAULT_FONT = "freesansbold.ttf"
_cachedFonts = {}

def init():
    pygame.font.init()
    loadFont("default", DEFAULT_FONT, 24)

def loadFont(name, fontPath, fontSize):
    _cachedFonts[name] = pygame.font.Font(FONT_LOAD_TEMPLATE % fontPath, fontSize)

def renderTextSurface(text, fontKey="default", color=colors.WHITE):
    return _cachedFonts[fontKey].render(text, True, color) if fontKey in _cachedFonts else None
