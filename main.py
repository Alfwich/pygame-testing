import pygame, sys, os, colors, time, random, images, fonts, sounds, events
import StaticObject, RenderList, Camera
import SOFrog, SOStaticText
from pygame.locals import *

FPS = 60
SCREEN_SIZE = (1000, 1000)
TITLE = "Test Game"

images.addToGlobalLoadList([
])

sounds.addToGlobalLoadList([
    ("startup", "windows-logon.wav")
])

# Inits pygame and various components
def init():
    pygame.init()
    images.init()
    fonts.init()
    colors.init()
    events.init()
    pygame.display.set_caption(TITLE)

    # Init images from their respective lists. This allows game classes
    # to define images and sounds that will be used at declaration time
    images.loadGlobalImageList()
    sounds.loadGlobalSoundList()

def getRandomCoord():
    return (random.randint(0, SCREEN_SIZE[0]), random.randint(0, SCREEN_SIZE[1]))

def main():
    init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    if screen is None or clock is None:
        print("Could not create screen or clock object.", screen, clock)
        return

    mainRenderList = RenderList.RenderList()
    mainCamera = Camera.Camera()
    mainCamera.locked = True

    frogObject = SOFrog.SOFrog()
    mainRenderList.addObject(frogObject)

    coolText = SOStaticText.SOStaticText("Cool Text; Brah!")
    mainRenderList.addObject(coolText)

    def spawnNewFrog(event):
        newFrog = SOFrog.SOFrog()
        newFrogPosition = mainCamera.transformScreenPosition(event.pos)
        newFrog.setPosition(newFrogPosition[0], newFrogPosition[1])
        mainRenderList.addObject(newFrog)

    def quitApplication(event):
        pygame.quit()
        sys.exit()

    events.bindQuitEvent(quitApplication)
    events.bindKeyDownEvent(["q"], quitApplication)
    events.bindMouseMotionEvent(lambda e: mainCamera.moveOffset(e.rel[0], e.rel[1]))
    events.bindMouseDownEvent([1], lambda e: mainCamera.unlock())
    events.bindMouseUpEvent([1], lambda e: mainCamera.lock())
    events.bindMouseDownEvent([3], spawnNewFrog)
    events.bindKeyDownEvent(["g"], lambda e: sounds.playSoundOnce("startup"))
    #print events._callbacks
    while True:
        # Limit framerate to the desired FPS
        delta = clock.tick(FPS)/1000.0

        # Handle game events through the event queue
        events.handleEvents()

        # Call the tick methos from any tickable object
        events.tickObjects(delta)

        # Draw screen
        #screen.fill(colors.getColor(colors.BLACK))
        mainRenderList.render(screen, mainCamera)
        pygame.display.update()

if __name__ == "__main__":
    main()
