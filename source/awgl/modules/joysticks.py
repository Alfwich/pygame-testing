import pygame
import events

_joysticks = {
    "count": 0,
    "joys": []
}

def _unbindAllJoysticks():
    for js in _joysticks["joys"]:
        js.quit()

def _bindAllJoysticks():
    _joysticks["joys"] = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    [js.init() for js  in _joysticks["joys"]]

def init():
    pygame.joystick.init()

def updateJoysticks():
    #_unbindAllJoysticks()
    pygame.joystick.quit()
    pygame.joystick.init()
    _bindAllJoysticks()
    _joysticks["count"] = len(_joysticks["joys"])
    return numberOfJoysticks()

def numberOfJoysticks():
    return 10#_joysticks["count"]

def getControllerName(controllerId):
    return _joysticks["joys"][controllerId].get_name()
