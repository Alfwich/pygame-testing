import pygame, sys, os, math, random, time

# If we are running in the executable dist then make sure that python is
# using the executable path as the orgin for file requests.
if not "__file__" in locals():
    newPath = "\\".join(str(sys.executable).split("\\")[:-1])
    os.chdir(newPath)

from source.awgl.modules import *
from source.awgl.objs import *
from source.game import *

TITLE = "Test Game"

images.addToGlobalLoadList([
])

sounds.addToGlobalLoadList([
    ("startup", "windows-logon.wav")
])

# Inits pygame and various components
def initScreen():
    return pygame.display.set_mode(SCREEN_SIZE, SCREEN_FLAGS)

def init():
    [ mod.init() for mod in [pygame, images, fonts, joysticks, display] ]
    display.setFPS(30)
    # Init images from their respective lists. This allows game classes
    # to define images and sounds that will be used at declaration time
    images.loadGlobalImageList()
    sounds.loadGlobalSoundList()

def frameLimit(clock, busy=False):
    return clock.tick(display.getDesiredFPS())/1000.0

def main():
    init()
    clock = pygame.time.Clock()

    hudRenderList = RenderList.RenderList("hud")
    playerRenderList = RenderList.RenderList("player")
    worldRenderList = RenderList.RenderList("world")
    particleRenderList = RenderList.RenderList("particle")
    mainCamera = Camera.Camera()
    mainCamera.locked = False

    tileSize = 100
    tiles = []
    def updateRandomTiles():
        for tile in tiles:
            tile.disable()

        while len(tiles):
            tiles.pop(0)

        worldRenderList.removeAll()
        for x in range(0, display.getScreenWidth(), tileSize):
            for y in range(0, display.getScreenHeight(), tileSize):
                newMetalTile = SOMetalTile.SOMetalTile(tileSize, tileSize)
                newMetalTile.setPosition(x, y)
                tiles.append(newMetalTile)
                worldRenderList.addObject(newMetalTile)
    updateRandomTiles()
    events.bindVideoChangeEvent(lambda e: updateRandomTiles())


    coolText = SOStaticText.SOStaticText(display.getScreenSize())
    hudRenderList.addObject(coolText)
    events.bindVideoChangeEvent(lambda e: coolText.updateText(display.getScreenSize()))

    def quitApplication():
        pygame.quit()
        sys.exit()
    events.bindQuitEvent(lambda e: quitApplication())
    events.bindKeyDownEvent(["q"], lambda e: quitApplication())

    players = []
    def updatePlayers(event=None):
        numberOfPlayers = joysticks.updateJoysticks()
        while len(players):
            players[0].disable()
            players.pop(0)
        playerRenderList.removeAll()
        for i in range(0, numberOfPlayers):
            animatedGuy = AOWalkingGuy.AOWalkingGuy(i)
            animatedGuy.addPosition(i*(500/numberOfPlayers), 0)
            playerRenderList.addObject(animatedGuy)
            players.append(animatedGuy)
    events.bindKeyDownEvent(["l"], updatePlayers)
    updatePlayers()

    events.bindKeyDownEvent(["f"], lambda e: display.toggleFullscreen())
    events.bindKeyDownEvent(["g"], lambda e: display.decreaseScreenMode())
    events.bindKeyDownEvent(["h"], lambda e: display.increaseScreenMode())
    events.bindKeyDownEvent(["t"], lambda e: display.setSmallestResolution())
    events.bindKeyDownEvent(["y"], lambda e: display.setLargestResolution())
    events.bindKeyDownEvent(["o"], lambda e: sounds.playSoundOnce("startup"))
    while True:
        # Limit framerate to the desired FPS
        delta = frameLimit(clock)

        # Handle game events through the event queue and tick all game constructs
        events.handleEvents()
        events.tick(delta)

        # Draw screen
        screen = display.getScreen()
        screen.fill(colors.PURPLE)
        worldRenderList.render(screen, mainCamera)
        playerRenderList.render(screen, mainCamera)
        particleRenderList.render(screen, mainCamera)
        hudRenderList.render(screen, mainCamera)
        pygame.display.update()

if __name__ == "__main__":
    main()
