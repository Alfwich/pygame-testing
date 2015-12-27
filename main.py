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
    ("test-image", "test.png"),
    ("tracer", "tracer.png")
])

sounds.addToGlobalLoadList([
    ("startup", "windows-logon.wav")
])

# Inits pygame and various components
def initScreen():
    return pygame.display.set_mode(SCREEN_SIZE, SCREEN_FLAGS)

def init():
    [mod.init() for mod in [pygame, images, fonts, sounds, joysticks, display, clock]]
    #display.setFPS(30)

def main():
    init()
    gs = GameState.GameState()
    GameState.GameState.setGlobalGameState(gs)
    hudRenderList = RenderList.RenderList("hud")
    playerRenderList = SortedRenderList.SortedRenderList("player")
    powerupRenderList = RenderList.RenderList("powerups")
    worldRenderList = RenderList.RenderList("world")
    particleRenderList = RenderList.RenderList("particle")
    mainCamera = Camera.Camera()
    hudCamera = Camera.Camera()

    infoText = TInfoText.TInfoText()
    hudRenderList.addObject(infoText)

    def quitApplication():
        pygame.quit()
        sys.exit()
    events.bindQuitEvent(lambda e: quitApplication())
    events.bindKeyDownEvent(["q"], lambda e: quitApplication())

    tileMap = TileMap.TileMap("test1.json")
    worldRenderList.addObject(tileMap)
    gs.world = tileMap

    players = []
    def updatePlayers(event=None):
        numberOfPlayers = joysticks.updateJoysticks()
        #numberOfPlayers = 200
        spawnLocations = gs.world.getTiles("spawn")
        random.shuffle(spawnLocations)
        if numberOfPlayers == 0:
            numberOfPlayers = 1
        while len(players):
            players[0].disabled = True
            players.pop(0)
        playerRenderList.removeAll()
        for i in range(0, numberOfPlayers):
            animatedGuy = AOPlayerCharacter.AOPlayerCharacter(i, spawnLocations.pop()[0])
            playerRenderList.addObject(animatedGuy)
            players.append(animatedGuy)
    events.bindKeyDownEvent(["l"], updatePlayers)
    events.bindJoystickButtonUpEvent(0, 5, updatePlayers)
    updatePlayers()

    powerups = []
    def updatePowerups(event=None):
        while len(powerups):
            powerups[0].disabled = True
            powerups.pop(0)

        powerupLocations = gs.world.getTiles("powerups")
        for tile in powerupLocations:
            powerup = SOPowerUp.SOPowerUp(tile[0])
            powerups.append(powerup)
            powerupRenderList.addObject(powerup)

    events.bindKeyDownEvent(["l"], updatePowerups)
    events.bindJoystickButtonUpEvent(0, 5, updatePowerups)
    updatePowerups()

    def loadLevel(level):
        tileMap.loadMap(level)
        updatePlayers()
        updatePowerups()

    events.bindKeyDownEvent(["1"], lambda e, l: loadLevel(l), "default.json")
    events.bindKeyDownEvent(["2"], lambda e, l: loadLevel(l), "test1.json")
    events.bindKeyDownEvent(["3"], lambda e, l: loadLevel(l), "test2.json")
    events.bindKeyDownEvent(["f"], lambda e: display.toggleFullscreen())
    events.bindKeyDownEvent(["g"], lambda e: display.decreaseScreenMode())
    events.bindKeyDownEvent(["h"], lambda e: display.increaseScreenMode())
    events.bindKeyDownEvent(["t"], lambda e: display.setSmallestResolution())
    events.bindKeyDownEvent(["y"], lambda e: display.setLargestResolution())
    events.bindKeyDownEvent(["o"], lambda e: sounds.playSoundOnce("startup"))
    events.bindTimer(events.printContainerSizes, 250, -1)

    while True:
        # Limit framerate to the desired FPS
        delta = clock.tick()

        # Handle game events through the event queue and tick all game constructs
        events.handleEvents()
        events.tick(delta)

        mainCamera.centerOnObject(players[0])

        # Draw screen
        screen = display.getScreen()
        #screen.fill(colors.BLACK)
        worldRenderList.render(screen, mainCamera)
        playerRenderList.render(screen, mainCamera)
        powerupRenderList.render(screen, mainCamera)
        particleRenderList.render(screen, mainCamera)
        hudRenderList.render(screen, hudCamera)
        for obj in gs.getCollisions(pygame.Rect(0,0,200000,200000), None):
            objRect = pygame.Rect(obj.rect)
            mainCamera.transformRectWorldPosition(objRect)
            pygame.draw.lines(screen, colors.DEBUG, True, [objRect.topleft, objRect.topright, objRect.bottomright, objRect.bottomleft], 2)
        pygame.display.update()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "profile":
        import cProfile, pstats
        cProfile.run("main()", "profile.generated.log")
        out = open("profile.output.log", "w")
        p = pstats.Stats('profile.generated.log', stream=out)
        p.strip_dirs().sort_stats('tottime')
        p.print_stats()

    else:
        main()
