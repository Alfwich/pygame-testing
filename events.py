import pygame, types
from pygame.locals import *

_callbacks = {}
_tickableObjects = []

LEFT_MOUSE_BUTTON = 1
RIGHT_MOUSE_BUTTON = 3

def _processKeysArray(keys):
    keyOrds = []

    if not isinstance(keys, list):
        keys = [keys]

    for key in keys:
        if key in globals() and isinstance(globals()[key], int):
            keyOrds.append(globals()[key])
        elif isinstance(key, str):
            keyOrds.append(ord(key[0]))
        elif isinstance(key, int):
            keyOrds.append(key)
        else:
            print("Attempted to bind function with activation key: %s, but could not fine a way to convert to a key ord." % key)

    return set(keyOrds)

def _processButtonsArray(buttons):
    buttonOrds = []

    if not isinstance(buttons, list):
        buttons = [buttons]

    for button in buttons:
        if isinstance(button, int):
            buttonOrds.append(button)
        elif button in locals() and isinstance(locals()[button], int):
            buttonOrds.append(locals()[button])
        else:
            print("Attempted to bind function with activation button: %s, but could not fine a way to convert to a button ord." % button)

    return set(buttonOrds)

def _copyFunction(f):
    return types.FunctionType(f.func_code, f.func_globals, f.func_name, f.func_defaults, f.func_closure)

def init():
    pygame.init()

def handleEvents():
    for e in pygame.event.get():
        if e.type in _callbacks:
            for callback in _callbacks[e.type]:
                callback(e)

def tickObjects(delta=None):
    for obj in _tickableObjects:
        if obj._shouldTick and obj._isValid:
            obj.tick(delta)

def registerTickableObject(obj):
    _tickableObjects.append(obj)

def _bindEvent(action, callback):
    if action not in _callbacks:
        _callbacks[action] = []
    _callbacks[action].append(callback)

def bindQuitEvent(callback, obj=None):
    def quitEventWrapper(event):
        pramList = (event,) if obj is None else (event, obj)
        callback(*pramList)

    _bindEvent(QUIT, quitEventWrapper)

def bindKeyAxis(downKeys, upKeys, callback, obj=None):
    downKeyOrds = _processKeysArray(downKeys)
    upKeyOrds = _processKeysArray(upKeys)
    combinedOrds = downKeyOrds | upKeyOrds

    def keyAxisWrapper(event):
        if event.key in combinedOrds:
            val = 0 if event.type == KEYUP else 1 if event.key in upKeyOrds else -1
            pramList = (event, val) if obj is None else (event, val, obj)
            callback(*pramList)

    _bindEvent(KEYUP, keyAxisWrapper)
    _bindEvent(KEYDOWN, keyAxisWrapper)

def bindKeyUpEvent(keys, callback, obj=None):
    keyOrds = _processKeysArray(keys)

    def keydownWrapper(event):
        if event.key in keyOrds:
            pramList = (event,) if obj is None else (event, obj)
            callback(*pramList)

    _bindEvent(KEYUP, keydownWrapper)

def bindKeyDownEvent(keys, callback, obj=None):
    keyOrds = _processKeysArray(keys)

    def keyupWrapper(event):
        if event.key in keyOrds:
            pramList = (event,) if obj is None else (event, obj)
            callback(*pramList)

    _bindEvent(KEYDOWN, keyupWrapper)


def bindMouseDownEvent(buttons, callback, obj=None):
    buttonOrds = _processButtonsArray(buttons)

    def mouseDownWrapper(event):
        if event.button in buttonOrds:
            pramList = (event,) if obj is None else (event, obj)
            callback(*pramList)

    _bindEvent(MOUSEBUTTONDOWN, mouseDownWrapper)

def bindMouseUpEvent(buttons, callback, obj=None):
    buttonOrds = _processButtonsArray(buttons)

    def mouseUpWrapper(event):
        if event.button in buttonOrds:
            pramList = (event,) if obj is None else (event, obj)
            callback(*pramList)

    _bindEvent(MOUSEBUTTONUP, mouseUpWrapper)

def bindMouseMotionEvent(callback, obj=None):
    def mouseMotionEventWrapper(event):
        pramList = (event,) if obj is None else (event, obj)
        callback(*pramList)

    _bindEvent(MOUSEMOTION, mouseMotionEventWrapper)

def unbindEvents(action):
    if action in _callbacks:
        _callbacks[action] = []
