import pygame
import events

_joystickCount = 0
_joysticks = []

def _bindAllJoysticks():
    global _joysticks
    _joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    [js.init() for js  in _joysticks]

def init():
    pygame.joystick.init()

def updateJoysticks():
    global _joystickCount
    pygame.joystick.quit()
    pygame.joystick.init()
    _bindAllJoysticks()
    _joystickCount = len(_joysticks)
    return _joystickCount

def numberOfJoysticks():
    return _joystickCount

def getControllerName(controllerId):
    return _joysticks[controllerId].get_name()
