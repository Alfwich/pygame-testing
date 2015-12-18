import pygame, sys, os, colors, time, random, images, fonts, sounds, events, StaticObject, RenderList
from pygame.locals import *

FPS = 60
SCREEN_SIZE = (1000, 1000)
TITLE = "Test Game"
IMAGE_LOAD_LIST = [
    ("frog", "frog-face.png")
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

def bindEvents():
    def quitApplication(e):
        pygame.quit()
        sys.exit()

    events.bindEvent(QUIT, quitApplication)

def getRandomCoord():
    return (random.randint(0, SCREEN_SIZE[0]), random.randint(0, SCREEN_SIZE[1]))

def blitStaticObject(screen, staticObject):
    screen.blit(staticObject.getBitmap(), staticObject.getPosition())

def main():
    init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    mainRenderList = RenderList.RenderList()
    bindEvents()
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


    events.bindEvent(KEYDOWN, moveFrogKeyDown, frogObject)
    events.bindEvent(KEYUP, moveFrogKeyUp, frogObject)

    if screen is None or clock is None:
        print("Could not create screen or clock object.", screen, clock)
        return

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
