import pygame

_joysticks = {
    "count": 0,
    "joys": []
}

def init():
    pygame.init()
    updateJoysticks()

def updateJoysticks():
    numberOfJoysticks = pygame.joystick.get_count()
    if not numberOfJoysticks == _joysticks["count"]:
        _joysticks["joys"] = [pygame.joystick.Joystick(x) for x in xrange(pygame.joystick.get_count())]
        for js in _joysticks["joys"]:
            js.init()
