import pygame, types
from ..objs import Timeout
from pygame.locals import *

_callbacks = {}
_createdEventHandlers = set()
_tickableObjects = []
_timers = []

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

def _bindEvent(action, callback):
    _createdEventHandlers.add(id(callback))
    if action not in _callbacks:
        _callbacks[action] = []
    _callbacks[action].append(callback)

def _transformAnalogInput(value, deadZone):
    return value if abs(value) > deadZone else 0

def _handleTimers(delta):
    global _timers
    if len(_timers) > 0:
        shouldFilterTimers = False
        for idx, timer in enumerate(_timers):
            timer.tick(delta)
            if not timer.isValid():
                _timers[idx] = None
                shouldFilterTimers = True
        if shouldFilterTimers:
            _timers = filter(lambda x: x, _timers)

def handleEvents():
    for e in pygame.event.get():
        #print e
        if e.type in _callbacks:
            for callback in _callbacks[e.type]:
                callback(e)

def tick(delta=0.0):
    for obj in _tickableObjects:
        obj.tick(delta)

    _handleTimers(delta)

def registerTickableObject(obj):
    _tickableObjects.append(obj)

def deregisterTickableObject(obj):
    _tickableObjects.remove(obj)

def bindQuitEvent(callback, obj=None):
    def quitEventWrapper(event):
        pramList = (event,) if obj is None else (event, obj)
        callback(*pramList)

    _bindEvent(QUIT, quitEventWrapper)
    return id(bindQuitEvent)

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
    return id(keyAxisWrapper)

def bindKeyUpEvent(keys, callback, obj=None):
    keyOrds = _processKeysArray(keys)

    def keyUpWrapper(event):
        if event.key in keyOrds:
            pramList = (event,) if obj is None else (event, obj)
            callback(*pramList)

    _bindEvent(KEYUP, keyUpWrapper)
    return id(keyUpWrapper)

def bindKeyDownEvent(keys, callback, obj=None):
    keyOrds = _processKeysArray(keys)

    def keyDownWrapper(event):
        if event.key in keyOrds:
            pramList = (event,) if obj is None else (event, obj)
            callback(*pramList)

    _bindEvent(KEYDOWN, keyDownWrapper)
    return id(keyDownWrapper)

def bindMouseDownEvent(buttons, callback, obj=None):
    buttonOrds = _processButtonsArray(buttons)

    def mouseDownWrapper(event):
        if event.button in buttonOrds:
            pramList = (event,) if obj is None else (event, obj)
            callback(*pramList)

    _bindEvent(MOUSEBUTTONDOWN, mouseDownWrapper)
    return id(mouseDownWrapper)

def bindMouseUpEvent(buttons, callback, obj=None):
    buttonOrds = _processButtonsArray(buttons)

    def mouseUpWrapper(event):
        if event.button in buttonOrds:
            pramList = (event,) if obj is None else (event, obj)
            callback(*pramList)

    _bindEvent(MOUSEBUTTONUP, mouseUpWrapper)
    return id(mouseUpWrapper)

def bindMouseMotionEvent(callback, obj=None):
    def mouseMotionEventWrapper(event):
        pramList = (event,) if obj is None else (event, obj)
        callback(*pramList)

    _bindEvent(MOUSEMOTION, mouseMotionEventWrapper)
    return id(mouseMotionEventWrapper)

def bindJoystickAxisMotionEvent(joystick, axis, callback, deadZone=0.2, obj=None):
    def joystickMotionEventWrapper(event):
        if event.joy == joystick and event.axis == axis:
            value = _transformAnalogInput(event.value, deadZone)
            pramList = (event, value) if obj is None else(event, value, obj)
            callback(*pramList)

    _bindEvent(JOYAXISMOTION, joystickMotionEventWrapper)
    return id(joystickMotionEventWrapper)

def bindJoystickButtonDownEvent(joystick, buttons, callback, obj=None):
    buttonOrds = _processButtonsArray(buttons)
    def joystickButtonDownEventWrapper(event):
        if event.joy == joystick and event.button in buttonOrds:
            prams = (event,) if obj is None else (event, obj)
            callback(*prams)

    _bindEvent(JOYBUTTONDOWN, joystickButtonDownEventWrapper)
    return id(joystickButtonDownEventWrapper)

def bindJoystickButtonUpEvent(joystick, buttons, callback, obj=None):
    buttonOrds = _processButtonsArray(buttons)
    def joystickButtonUpEventWrapper(event):
        if event.joy == joystick and event.button in buttonOrds:
            prams = (event,) if obj is None else (event, obj)
            callback(*prams)

    _bindEvent(JOYBUTTONUP, joystickButtonUpEventWrapper)
    return id(joystickButtonUpEventWrapper)

def bindJoystickButtonAxis(joystick, downButtons, upButtons, callback, obj=None):
    downButtonOrds = _processKeysArray(downButtons)
    upButtonOrds = _processKeysArray(upButtons)
    combinedOrds = downButtonOrds | upButtonOrds

    def joystickButtonAxisWrapper(event):
        if event.joy == joystick and event.button in combinedOrds:
            val = 0 if event.type == JOYBUTTONUP else 1 if event.button in upButtonOrds else -1
            pramList = (event, val) if obj is None else (event, val, obj)
            callback(*pramList)

    _bindEvent(JOYBUTTONUP, joystickButtonAxisWrapper)
    _bindEvent(JOYBUTTONDOWN, joystickButtonAxisWrapper)
    return id(joystickButtonAxisWrapper)

def bindVideoChangeEvent(callback, obj=None):
    def videoExposeEventWrapper(event):
        pramList = (event,) if obj is None else (event, obj)
        callback(*pramList)

    _bindEvent(VIDEOEXPOSE, videoExposeEventWrapper)
    return id(videoExposeEventWrapper)

def _removeEventFromBoundEvents(eventHandle):
    for eventType in _callbacks:
        for event in _callbacks[eventType]:
            if id(event) == eventHandle:
                _callbacks[eventType].remove(event)
                _createdEventHandlers.remove(eventHandle)
                return True

def unbindEvent(eventHandles):
    if not isinstance(eventHandles, list):
        eventHandles = [eventHandles]

    for eventHandle in eventHandles:
        if eventHandle in _createdEventHandlers:
            _removeEventFromBoundEvents(eventHandle)


    return False

def bindTimer(callback, time, repeats=False):
    newTimeout = Timeout.Timeout(callback, time, repeats)
    _timers.append(newTimeout)
    return id(newTimeout)

def unbindTimer(timerId):
    for timeout in _timers:
        if id(timeout) == timerId:
            _timers.remove(timeout)
            return
