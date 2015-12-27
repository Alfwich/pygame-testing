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

def shuffled(lst):
    random.shuffle(lst)
    return lst

# Inits pygame and various components
def initScreen():
    return pygame.display.set_mode(SCREEN_SIZE, SCREEN_FLAGS)

def init():
    return [mod.init() for mod in [pygame, images, fonts, sounds, joysticks, display, clock]]

def main():
    init()
    gs = GameState.GameState()
    GameState.GameState.setGlobalGameState(gs)
    mainRenderList = gs.renderList
    hudRenderList = RenderList.RenderList("hud")
    worldRenderList = RenderList.RenderList("world")
    worldRenderList.add(gs.world)
    particleRenderList = RenderList.RenderList("particle")
    mainCamera = Camera.Camera()
    hudCamera = Camera.Camera()

    infoText = TInfoText.TInfoText()
    hudRenderList.add(infoText)

    screenFader = SOScreenFader.SOScreenFader(fadeSpeed=255)
    screenFader.fadeOut()
    hudRenderList.add(screenFader)

    def quitApplication():
        pygame.quit()
        sys.exit()
    events.bindQuitEvent(lambda e: quitApplication())
    events.bindKeyDownEvent(["q"], lambda e: quitApplication())


    def updatePlayers(event=None):
        numberOfPlayers = joysticks.updateJoysticks() or 10
        numberOfPlayers = 10
        spawnLocations = shuffled(gs.world.getTiles("spawn"))
        gs["currentPlayerIndex"] = 0
        gs["players"] = [gs.createGameObject(AOPlayerCharacter.AOPlayerCharacter, player=i, location=spawnLocations.pop()[0]) for i in range(numberOfPlayers)]

    def updatePowerups(event=None):
        [gs.createGameObject(SOPowerUp.SOPowerUp, location=tile[0]) for tile in gs.world.getTiles("powerups")]

    def loadLevel(level):
        screenFader.fadeIn()
        def loadLevelWrapper():
            gs.loadMap(level)
            updatePlayers()
            updatePowerups()
            screenFader.fadeOut()
        events.bindTimer(loadLevelWrapper, 1500)

    def nextPlayer():
        gs["currentPlayerIndex"] = (gs["currentPlayerIndex"] + 1) % len(gs["players"])
    events.bindJoystickButtonDownEvent(0, 5, lambda e: nextPlayer())

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

    gs.loadMap("test1.json")
    updatePlayers()
    updatePowerups()
    screenFader.fadeOut()

    while True:
        # Limit framerate to the desired FPS
        delta = clock.tick()

        # Handle game events through the event queue and tick all game constructs
        events.handleEvents()
        events.tick(delta)

        mainCamera.centerOnObject(gs["players"][gs["currentPlayerIndex"]])

        # Draw screen
        screen = display.getScreen()
        #screen.fill(colors.BLACK)
        worldRenderList.render(screen, mainCamera)

        mainRenderList.render(screen, mainCamera)
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
