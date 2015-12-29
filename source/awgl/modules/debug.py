import pygame
import colors, events

DEBUG = True
def doNothing(*args, **kwargs):
    pass

def debugSwitch(func):
    return func if DEBUG else doNothing

@debugSwitch
def init():
    events.bindTimer(printEventContainerSizes, 250, -1)

@debugSwitch
def renderGameStateCollisionRects(screen, gameState, mainCamera):
    for obj in gameState.getCollisions(pygame.Rect(0,0,200000,200000), None):
        objRect = pygame.Rect(obj.rect)
        mainCamera.transformRectWorldPosition(objRect)
        pygame.draw.lines(screen, colors.DEBUG, True, [objRect.topleft, objRect.topright, objRect.bottomright, objRect.bottomleft], 2)

@debugSwitch
def printEventContainerSizes():
    print("Event Information: %s" % events.getContainerSizeString())

@debugSwitch
def printDisplayInfo():
    print pygame.display.Info()
