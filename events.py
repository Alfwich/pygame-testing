import pygame, types
from pygame.locals import *

_callbacks = {}
_tickableObjects = []

LEFT_MOUSE_BUTTON = 1
RIGHT_MOUSE_BUTTON = 3

def init():
    pygame.init()

def copyFunction(f):
    return types.FunctionType(f.func_code, f.func_globals, f.func_name, f.func_defaults, f.func_closure)

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

def createBoundFunction(obj, fun):
    newFunction = copyFunction(fun)
    newFunction._binder = obj
    return newFunction

def bindEvent(action, callback, obj=None):
    if not hasattr(callback, "im_self") and not obj is None:
        callback = createBoundFunction(obj, callback)

    if action not in _callbacks:
        _callbacks[action] = []

    _callbacks[action].append(callback)

def bindKeyUpEvent(keys, callback, obj=None):
    if not hasattr(callback, "im_self") and not obj is None:
        callback = createBoundFunction(obj, callback)

    keys = map(lambda x: ord(x), keys)

    def keydownFilter(event):
        if event.key in keys:
            if hasattr(callback, "_binder"):
                callback(event, callback._binder)
            else:
                callback(event)

    bindEvent(KEYUP, keydownFilter)

def bindKeyDownEvent(keys, callback, obj=None):
    if not hasattr(callback, "im_self") and not obj is None:
        callback = createBoundFunction(obj, callback)

    keys = map(lambda x: ord(x), keys)

    def keyupFilter(event):
        if event.key in keys:
            if hasattr(callback, "_binder"):
                callback(event, callback._binder)
            else:
                callback(event)

    bindEvent(KEYDOWN, keyupFilter)

def bindMouseDownEvent(buttons, callback, obj=None):
    if not hasattr(callback, "im_self") and not obj is None:
        callback = createBoundFunction(obj, callback)

    def mouseDownFilter(event):
        if event.button in buttons:
            if hasattr(callback, "_binder"):
                callback(event, callback._binder)
            else:
                callback(event)

    bindEvent(MOUSEBUTTONDOWN, mouseDownFilter)

def bindMouseUpEvent(buttons, callback, obj=None):
    if not hasattr(callback, "im_self") and not obj is None:
        callback = createBoundFunction(obj, callback)

    def mouseUpFilter(event):
        if event.button in buttons:
            if hasattr(callback, "_binder"):
                callback(event, callback._binder)
            else:
                callback(event)

    bindEvent(MOUSEBUTTONUP, mouseUpFilter)

def bindMouseMotionEvent(callback, obj=None):
    if not hasattr(callback, "im_self") and not obj is None:
        callback = createBoundFunction(obj, callback)

    bindEvent(MOUSEMOTION, callback)

def unbindEvents(action, obj=None):
    if action in _callbacks:
        for idx, callback in enumerate(_callbacks[action]):
            if obj is None or callback._binder is obj:
                _callbacks[action][idx] = None
        _callbacks[action] = filter(lambda x: x, _callbacks[action])

def registerTickableObject(obj):
    _tickableObjects.append(obj)
