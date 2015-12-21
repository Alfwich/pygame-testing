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
    for js in _joysticks["joys"]:
        js.init()

def init():
    pygame.joystick.init()
    updateJoysticks()
    events.bindTimer(updateJoysticks, 1000, -1)

def updateJoysticks():
    print "Updated joysticks"
    numberOfJoysticks = pygame.joystick.get_count()
    if not numberOfJoysticks == _joysticks["count"]:
        _joysticks["count"] = numberOfJoysticks
        _unbindAllJoysticks()
        _bindAllJoysticks()
