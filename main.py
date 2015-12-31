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
    renderer._openGlEnabled = True
    return [mod.init() for mod in [pygame, display, images, fonts, sounds, joysticks, clock, debug]]

def main():
    init()
    gs = GameState.GameState()
    GameState.GameState.setGlobalGameState(gs)
    mainRenderList = gs.renderList
    hudRenderList = RenderList.RenderList("hud")
    worldRenderList = RenderList.RenderList("world")
    worldRenderList.add(gs.world)
    overRenderList = RenderList.RenderList("over")
    particleRenderList = RenderList.RenderList("particle")
    mainCamera = Camera.Camera()
    mainCamera.priority = 15
    mainCamera.transitionDuration = 0.2
    hudCamera = Camera.Camera()

    infoText = TInfoText.TInfoText()
    hudRenderList.add(infoText)

    objectTargeter = DOTargetRect.DOTargetRect()
    overRenderList.add(objectTargeter)

    screenFader = DOScreenFader.DOScreenFader(fadeSpeed=255)
    screenFader.fadeOut()
    hudRenderList.add(screenFader)

    def quitApplication():
        pygame.quit()
        sys.exit()
    events.bindQuitEvent(lambda e: quitApplication())
    events.bindKeyDownEvent(["q"], lambda e: quitApplication())

    def updatePlayers(event=None):
        numberOfPlayers = 10
        spawnLocations = shuffled(gs.world.getTiles("spawn"))
        gs["currentPlayerIndex"] = 0
        gs["players"] = [gs.createGameObject(AOPlayerCharacter.AOPlayerCharacter, player=i, location=spawnLocations.pop()[0]) for i in range(numberOfPlayers)]

    def updateCameraTarget(event=None):
        mainCamera.target = objectTargeter.target = gs["players"][gs["currentPlayerIndex"]]
        mainCamera.forceFinishAnimation()

    def updatePowerups(event=None):
        [gs.createGameObject(SOPowerUp.SOPowerUp, location=tile[0]) for tile in gs.world.getTiles("powerups")]

    def loadLevel(level):
        if not screenFader.isAnimating:
            screenFader.fadeIn(level)
            def loadLevelWrapper():
                gs.loadMap(level)
                levelPostLoad()
            events.bindTimer(loadLevelWrapper, screenFader.estimatedFadeTime)

    def nextPlayer():
        players = gs["players"]
        if len(players) > 1:
            gs["currentPlayerIndex"] = (gs["currentPlayerIndex"] + 1) % len(players)
            mainCamera.target = objectTargeter.target = players[gs["currentPlayerIndex"]]

    def prevPlayer():
        players = gs["players"]
        if len(players) > 1:
            gs["currentPlayerIndex"] = len(players)-1 if gs["currentPlayerIndex"] == 0 else gs["currentPlayerIndex"]-1
            mainCamera.target = objectTargeter.target = players[gs["currentPlayerIndex"]]

    def levelPostLoad():
        updatePlayers()
        updatePowerups()
        screenFader.fadeOut()
        updateCameraTarget()

    events.bindKeyDownEvent(["e"], lambda e: prevPlayer())
    events.bindJoystickButtonDownEvent(0, 5, lambda e: prevPlayer())

    events.bindKeyDownEvent(["r"], lambda e: nextPlayer())
    events.bindJoystickButtonDownEvent(0, 4, lambda e: nextPlayer())

    events.bindKeyDownEvent(["1"], lambda e, l: loadLevel(l), "default.json")
    events.bindKeyDownEvent(["2"], lambda e, l: loadLevel(l), "test1.json")
    events.bindKeyDownEvent(["3"], lambda e, l: loadLevel(l), "test2.json")
    events.bindKeyDownEvent(["4"], lambda e, l: loadLevel(l), "test3.json")
    events.bindKeyDownEvent(["f"], lambda e: display.toggleFullscreen())
    events.bindKeyDownEvent(["g"], lambda e: display.decreaseScreenMode())
    events.bindKeyDownEvent(["h"], lambda e: display.increaseScreenMode())
    events.bindKeyDownEvent(["t"], lambda e: display.setSmallestResolution())
    events.bindKeyDownEvent(["y"], lambda e: display.setLargestResolution())
    events.bindKeyDownEvent(["o"], lambda e: sounds.playSoundOnce("startup"))
    events.bindKeyDownEvent(["="], lambda e: renderer.disableOpenGL())
    events.bindKeyDownEvent(["-"], lambda e: renderer.enableOpenGL())
    events.bindTimer(joysticks.updateJoysticks, 1000, -1)
    #events.bindTimer(debug.printDisplayInfo, 500, -1)

    gs.loadMap("test3.json")
    levelPostLoad()

    while True:

        # Limit framerate to the desired FPS
        delta = clock.tick()

        # Handle game events through the event queue and tick all game constructs
        events.handleEvents()
        events.tick(delta)

        # Draw screen
        screen = display.getScreen()
        renderer.clear()
        worldRenderList.render(screen, mainCamera)
        mainRenderList.render(screen, mainCamera)
        overRenderList.render(screen, mainCamera)
        particleRenderList.render(screen, mainCamera)
        #debug.renderGameStateCollisionRects(screen, gs, mainCamera)
        hudRenderList.render(screen, hudCamera)
        renderer.update()

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
