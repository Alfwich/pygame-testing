import pygame, colors

DEFAULT_FONT_KEY = "__DEFAULT__"
FONT_COLOR_KEY = "current_font_color"
FONT_KEY_KEY = "current_font_key"
_loadedFonts = {}
_config = {
    FONT_COLOR_KEY: colors.WHITE,
    FONT_KEY_KEY: DEFAULT_FONT_KEY,
}

def init():
    _loadedFonts[DEFAULT_FONT_KEY] = loadFont('freesansbold.ttf', 32)

def loadFont(fontPath, fontSize):
    return pygame.font.Font(fontPath, fontSize)

def setCurrentRenderColor(color):
    _config[FONT_COLOR_KEY] = color

def setCurrentFont(fontKey):
    if fontKey in _loadedFonts:
        _config[FONT_KEY_KEY] = fontKey

def renderTextSurface(text):
    font = _loadedFonts[_config[FONT_KEY_KEY]]
    fontColor = colors.getColor(_config[FONT_COLOR_KEY])

    return font.render(text, True, fontColor)
