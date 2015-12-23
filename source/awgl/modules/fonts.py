import pygame, colors

FONT_LOAD_TEMPLATE = "data/font/%s"
_cachedFonts = {}
_globalFontLoadList = [
    ("default", "freesansbold.ttf", 24)
]

def init():
    pygame.font.init()
    loadGlobalFontList()

def addToGlobalLoadList(newList):
    for asset in newList:
        _globalFontLoadList.append(asset)

def loadGlobalFontList():
    loadFontList(_globalFontLoadList)

def loadFontList(fontList):
    for asset in fontList:
        loadFont(*asset)

def getFont(name):
    return _cachedFonts[name] if name in _cachedFonts else None

def loadFont(name, fontPath, fontSize):
    _cachedFonts[name] = pygame.font.Font(FONT_LOAD_TEMPLATE % fontPath, fontSize)

def renderTextSurface(text, font=None, color=colors.WHITE, backgroundColor=colors.TRANSPARENT):
    prams = (text, True, color) if backgroundColor is colors.TRANSPARENT else (text, True, color, backgroundColor)
    return font.render(*prams) if not font is None else _cachedFonts["default"].render(*prams)
