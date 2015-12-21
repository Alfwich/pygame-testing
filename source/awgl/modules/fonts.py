import pygame, colors


FONT_LOAD_TEMPLATE = "src/font/%s"
DEFAULT_FONT_KEY = "__DEFAULT__"
FONT_COLOR_KEY = "current_font_color"
FONT_KEY_KEY = "current_font_key"
_loadedFonts = {}
_config = {
    FONT_COLOR_KEY: colors.WHITE,
    FONT_KEY_KEY: DEFAULT_FONT_KEY,
}

def init():
    pygame.init()
    _loadedFonts[DEFAULT_FONT_KEY] = loadFont('freesans.ttf', 32)

def loadFont(fontName, fontSize):
    fontPath = FONT_LOAD_TEMPLATE % fontName
    return pygame.font.Font(fontPath, fontSize)

def setCurrentRenderColor(color):
    _config[FONT_COLOR_KEY] = color

def setCurrentFont(fontKey):
    if fontKey in _loadedFonts:
        _config[FONT_KEY_KEY] = fontKey

def renderTextSurface(text):
    font = _loadedFonts[_config[FONT_KEY_KEY]]
    fontColor = _config[FONT_COLOR_KEY]

    return font.render(text, True, fontColor)
