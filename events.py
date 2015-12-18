import pygame, types

_callbacks = {}
_tickableObjects = []

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

def bindEvent(action, callback, obj=None):
    # Create a copy of a callback function with the bound object
    if not hasattr(callback, "im_self") and not obj is None:
        callback = copyFunction(callback)
        callback._binder = obj

    if action not in _callbacks:
        _callbacks[action] = []

    _callbacks[action].append(callback)

def unbindEvents(action, obj=None):
    if action in _callbacks:
        for idx, callback in enumerate(_callbacks[action]):
            if obj is None or callback._binder is obj:
                _callbacks[action][idx] = None
        _callbacks[action] = filter(lambda x: x, _callbacks[action])

def registerTickableObject(obj):
    _tickableObjects.append(obj)
