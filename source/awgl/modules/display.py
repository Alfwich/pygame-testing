import pygame

_screen = None
_screenModes = None
_fps = 1000
_title = "PyGame Testing"
_fullscreen = False
_screenSize = [1280, 800]
_currentScreenSize = 8
_screenFlags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.NOFRAME

def _updateScreen():
    global _screen
    _screen = pygame.display.set_mode(_screenSize, _screenFlags | (pygame.FULLSCREEN if _fullscreen else 0))

def _updateTitle():
    pygame.display.set_caption(_title)

def init():
    global _screenModes
    pygame.display.init()
    pygame.mouse.set_visible(False)
    _screenModes = pygame.display.list_modes()[::-1]
    _updateScreen()
    _updateTitle()

def getScreen():
    return _screen

def getScreenModesAvailable():
    return _screenModes

def increaseScreenMode():
    global _currentScreenSize
    modes = getScreenModesAvailable()
    if _currentScreenSize < len(modes)-1:
        _currentScreenSize += 1
        setScreenSize(modes[_currentScreenSize])

def decreaseScreenMode():
    global _currentScreenSize
    modes = getScreenModesAvailable()
    if _currentScreenSize > 1:
        _currentScreenSize -= 1
        setScreenSize(modes[_currentScreenSize])

def setLargestResolution():
    global _currentScreenSize
    modes = getScreenModesAvailable()
    _currentScreenSize = len(modes)
    setScreenSize(modes[-1])

def setSmallestResolution():
    global _currentScreenSize
    modes = getScreenModesAvailable()
    _currentScreenSize = 0
    setScreenSize(modes[0])

def setScreenSize(screenMode):
    global _screenSize
    _screenSize = screenMode
    _updateScreen()

def getScreenSize():
    return _screenSize

def getScreenWidth():
    return _screenSize[0]

def getScreenHeight():
    return _screenSize[1]

def setWindowTitle(newTitle):
    global _title
    _title = newTitle
    _updateTitle()

def setFPS(newFPS):
    global _fps
    _fps = newFPS

def getFPS():
    return

def getDesiredFPS():
    return _fps

def toggleFullscreen():
    global _fullscreen
    _fullscreen = not _fullscreen
    _updateScreen()
