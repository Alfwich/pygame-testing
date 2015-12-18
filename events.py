import pygame, types

_callbacks = {}
_tickableObjects = []

def init():
    pass

def copyFunction(f):
    return types.FunctionType(f.func_code, f.func_globals, f.func_name, f.func_defaults, f.func_closure)

def handleEvents():
    for e in pygame.event.get():
        if e.type in _callbacks:
            for callback in _callbacks[e.type]:
                if not callback._binder is None:
                    callback(e, callback._binder)
                else:
                    callback(e)

    for obj in _tickableObjects:
        obj.tick(0.0)

def bindEvent(action, callback, obj=None):
    boundFunction = copyFunction(callback)
    boundFunction._binder = obj
    if action not in _callbacks:
        _callbacks[action] = []

    _callbacks[action].append(boundFunction)

def unbindEvents(action, obj=None):
    if action in _callbacks:
        for idx, callback in enumerate(_callbacks[action]):
            if obj is None or callback._binder is obj:
                _callbacks[action][idx] = None
        _callbacks[action] = filter(lambda x: x, _callbacks[action])

def registerTickableObject(obj):
    _tickableObjects.append(obj)
