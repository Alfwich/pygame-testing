import pygame, types
from pygame.locals import *

_callbacks = {}
_tickableObjects = []

LEFT_MOUSE_BUTTON = 1
RIGHT_MOUSE_BUTTON = 3

def _createBoundFunction(obj, fun):
    newFunction = _copyFunction(fun)
    newFunction._binder = obj
    return newFunction

def _processKeysArray(keys):
    keyOrds = []

    if not isinstance(keys, list):
        keys = [keys]

    for key in keys:
        if isinstance(key, str):
            keyOrds.append(ord(key[0]))
        elif key in locals() and isinstance(locals()[key], int):
            keyOrds.append(locals()[key])
        elif isinstance(key, int):
            keyOrds.append(key)
        else:
            print("Attempted to bind function with activation key: %s, but could not fine a way to convert to a key ord." % key)

    return keyOrds

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

    return buttonOrds

def _copyFunction(f):
    return types.FunctionType(f.func_code, f.func_globals, f.func_name, f.func_defaults, f.func_closure)

def init():
    pygame.init()

def handleEvents():
    for e in pygame.event.get():
        if e.type in _callbacks:
            for callback in _callbacks[e.type]:
                if hasattr(callback, "_binder"):
                    callback(e, callback._binder)
                else:
                    callback(e)

def tickObjects(delta=None):
    for obj in _tickableObjects:
        if obj._shouldTick and obj._isValid:
            obj.tick(delta)

def registerTickableObject(obj):
    _tickableObjects.append(obj)



def bindEvent(action, callback, obj=None):
    if not hasattr(callback, "im_self") and not obj is None:
        callback = _createBoundFunction(obj, callback)

    if action not in _callbacks:
        _callbacks[action] = []

    _callbacks[action].append(callback)

def bindKeyUpEvent(keys, callback, obj=None):
    if not hasattr(callback, "im_self") and not obj is None:
        callback = _createBoundFunction(obj, callback)

    keyOrds = _processKeysArray(keys)

    def keydownFilter(event):
        if event.key in keyOrds:
            if hasattr(callback, "_binder"):
                callback(event, callback._binder)
            else:
                callback(event)

    bindEvent(KEYUP, keydownFilter)

def bindKeyDownEvent(keys, callback, obj=None):
    if not hasattr(callback, "im_self") and not obj is None:
        callback = _createBoundFunction(obj, callback)

    keyOrds = _processKeysArray(keys)

    def keyupFilter(event):
        if event.key in keyOrds:
            if hasattr(callback, "_binder"):
                callback(event, callback._binder)
            else:
                callback(event)

    bindEvent(KEYDOWN, keyupFilter)


def bindMouseDownEvent(buttons, callback, obj=None):
    if not hasattr(callback, "im_self") and not obj is None:
        callback = _createBoundFunction(obj, callback)

    buttonOrds = _processButtonsArray(buttons)

    def mouseDownFilter(event):
        if event.button in buttonOrds:
            if hasattr(callback, "_binder"):
                callback(event, callback._binder)
            else:
                callback(event)

    bindEvent(MOUSEBUTTONDOWN, mouseDownFilter)

def bindMouseUpEvent(buttons, callback, obj=None):
    if not hasattr(callback, "im_self") and not obj is None:
        callback = _createBoundFunction(obj, callback)

    buttonOrds = _processButtonsArray(buttons)

    def mouseUpFilter(event):
        if event.button in buttonOrds:
            if hasattr(callback, "_binder"):
                callback(event, callback._binder)
            else:
                callback(event)

    bindEvent(MOUSEBUTTONUP, mouseUpFilter)

def bindMouseMotionEvent(callback, obj=None):
    if not hasattr(callback, "im_self") and not obj is None:
        callback = _createBoundFunction(obj, callback)

    bindEvent(MOUSEMOTION, callback)

def unbindEvents(action, obj=None):
    if action in _callbacks:
        for idx, callback in enumerate(_callbacks[action]):
            if obj is None or callback._binder is obj:
                _callbacks[action][idx] = None
        _callbacks[action] = filter(lambda x: x, _callbacks[action])
