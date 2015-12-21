import pygame, sys, os, math, random, time

# If we are running in the executable dist then make sure that python is
# using the executable path as the orgin for file requests.
if not "__file__" in locals():
    newPath = "\\".join(str(sys.executable).split("\\")[:-1])
    os.chdir(newPath)

from source.awgl.modules import *
from source.awgl.objs import *
from source.game import *

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
    events.init()
    joysticks.init()
    pygame.display.set_caption(TITLE)

    # Init images from their respective lists. This allows game classes
    # to define images and sounds that will be used at declaration time
    images.loadGlobalImageList()
    sounds.loadGlobalSoundList()

def frameLimit(clock, fps):
    return clock.tick(fps)/1000.0

def main():
    init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    if screen is None or clock is None:
        print("Could not create screen or clock object.", screen, clock)
        return

    playerRenderList = RenderList.RenderList("player")
    worldRenderList = RenderList.RenderList("world")
    particleRenderList = RenderList.RenderList("particle")
    mainCamera = Camera.Camera()
    mainCamera.locked = False

    coolText = SOStaticText.SOStaticText("Hello World!")
    worldRenderList.addObject(coolText)

    tileSize = 10
    for x in range(0, SCREEN_SIZE[0], tileSize):
        for y in range(0, SCREEN_SIZE[1], tileSize):
            newMetalTile = SOMetalTile.SOMetalTile(tileSize, tileSize)
            newMetalTile.setPosition(x, y)
            worldRenderList.addObject(newMetalTile)

    def quitApplication(event):
        pygame.quit()
        sys.exit()

    players = []
    def updatePlayers():
        numberOfPlayers = joysticks.updateJoysticks()
        while len(players):
            players[0].disable()
            players.pop(0)
        playerRenderList.removeAll()
        for i in range(0, numberOfPlayers):
            animatedGuy = AOWalkingGuy.AOWalkingGuy(i)
            animatedGuy.addPosition(i*(SCREEN_SIZE[0]/numberOfPlayers), 0)
            playerRenderList.addObject(animatedGuy)
            players.append(animatedGuy)

    events.bindQuitEvent(quitApplication)
    events.bindKeyDownEvent(["q"], quitApplication)
    events.bindKeyDownEvent(["g"], lambda e: sounds.playSoundOnce("startup"))
    events.bindKeyDownEvent(["l"], lambda e: updatePlayers())
    updatePlayers()
    while True:
        # Limit framerate to the desired FPS
        delta = frameLimit(clock, FPS)

        # Handle game events through the event queue and tick all game constructs
        events.handleEvents()
        events.tick(delta)

        # Draw screen
        screen.fill(colors.BLACK)
        worldRenderList.render(screen, mainCamera)
        playerRenderList.render(screen, mainCamera)
        particleRenderList.render(screen, mainCamera)
        pygame.display.update()

if __name__ == "__main__":
    main()
