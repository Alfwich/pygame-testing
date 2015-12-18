import pygame, sys, os, colors, time, random, images, fonts, sounds, events
import StaticObject, RenderList, Camera
import SOFrog, SOStaticText
from pygame.locals import *

FPS = 1000
SCREEN_SIZE = (1000, 1000)
TITLE = "Test Game"
IMAGE_LOAD_LIST = [
    ("frog", "frog-face.png"),
    ("frog2", "funny-frog-face.png")
]

SOUND_LOAD_LIST = [
    ("startup", "windows-logon.wav")
]

# Inits pygame and various components
def init():
    pygame.init()
    fonts.init()
    colors.init()
    events.init()
    pygame.display.set_caption(TITLE)

    # Init images from list
    images.loadImageList(IMAGE_LOAD_LIST)
    sounds.loadSoundList(SOUND_LOAD_LIST)

def getRandomCoord():
    return (random.randint(0, SCREEN_SIZE[0]), random.randint(0, SCREEN_SIZE[1]))

def blitStaticObject(screen, staticObject):
    screen.blit(staticObject.getBitmap(), staticObject.getPosition())

def main():
    init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    if screen is None or clock is None:
        print("Could not create screen or clock object.", screen, clock)
        return

    mainRenderList = RenderList.RenderList()
    mainCamera = Camera.Camera()

    frogObject = SOFrog.SOFrog()
    mainRenderList.addObject(frogObject)

    coolText = SOStaticText.SOStaticText("Cool Text; Brah!")
    mainRenderList.addObject(coolText)

    def moveCameraMouseMotion(event, camera):
        camera.moveOffset(event.rel[0], event.rel[1])

    def quitApplication(event):
        pygame.quit()
        sys.exit()

    def quitApplicationKeyDown(event):
        if event.unicode == u"q":
            quitApplication(event)

    events.bindEvent(QUIT, quitApplication)
    events.bindEvent(KEYDOWN, quitApplicationKeyDown)
    events.bindEvent(KEYDOWN, frogObject.moveKeyDown)
    events.bindEvent(KEYUP, frogObject.moveKeyUp)
    events.bindEvent(KEYDOWN, frogObject.changeFaceKeyDown)
    events.bindEvent(MOUSEMOTION, moveCameraMouseMotion, mainCamera)
    sounds.playSoundOnce("startup")
    while True:
        # Limit framerate to the desired FPS
        delta = clock.tick(FPS)/1000.0

        # Handle game events through the event queue
        events.handleEvents()

        # Call the tick methos from any tickable object
        events.tickObjects(delta)

        # Draw screen
        #screen.fill(colors.getColor(colors.BLACK))
        mainRenderList.renderList(screen, mainCamera)
        pygame.display.update()

if __name__ == "__main__":
    main()
