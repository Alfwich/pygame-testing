import pygame, sys, os, colors, time, random, images, fonts, sounds, events, StaticObject, RenderList
from pygame.locals import *

FPS = 60
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
    frogObject = StaticObject.StaticObject()
    frogObject.setBitmap(images.getImage("frog"))
    mainRenderList.addObject(frogObject)

    coolText = StaticObject.StaticObject()
    coolText.setBitmap(fonts.renderTextSurface("Cool Text; Brah!"))
    mainRenderList.addObject(coolText)

    def moveFrogKeyDown(event, frog):
        if event.unicode == u"w":
            frog.velocity[1] = -1
        elif event.unicode == u"s":
            frog.velocity[1] = 1
        elif event.unicode == u"a":
            frog.velocity[0] = -1
        elif event.unicode == u"d":
            frog.velocity[0] = 1

    def moveFrogKeyUp(event, frog):
        if event.key in [ord("w"), ord("s")]:
            frog.velocity[1] = 0
        elif event.key in [ord("a"), ord("d")]:
            frog.velocity[0] = 0

    def moveTextMouseMotion(event, text):
        text.position = [event.pos[0], event.pos[1]]

    def quitApplication(event):
        pygame.quit()
        sys.exit()

    def quitApplicationKeyDown(event):
        if event.unicode == u"q":
            quitApplication(event)

    def changeFrogFaceKeyDown(event, frog):
        if event.unicode == u"o":
            frog.setBitmap(images.getImage("frog"))
        elif event.unicode == u"p":
            frog.setBitmap(images.getImage("frog2"))

    events.bindEvent(QUIT, quitApplication)
    events.bindEvent(KEYDOWN, quitApplicationKeyDown)
    events.bindEvent(KEYDOWN, moveFrogKeyDown, frogObject)
    events.bindEvent(KEYDOWN, changeFrogFaceKeyDown, frogObject)
    events.bindEvent(KEYUP, moveFrogKeyUp, frogObject)
    events.bindEvent(MOUSEMOTION, moveTextMouseMotion, coolText)
    sounds.playSoundOnce("startup")
    while True:
        # Limit framerate to the desired FPS
        clock.tick(FPS)

        # Handle game events and each object's tick function
        events.handleEvents()

        # Draw screen
        screen.fill(colors.getColor(colors.BLACK))
        mainRenderList.renderList(screen)
        pygame.display.update()

if __name__ == "__main__":
    main()
