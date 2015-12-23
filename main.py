import pygame
import sys
import os
import math
import random
import time

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
    [mod.init() for mod in [pygame, images, fonts, joysticks, display, clock]]
    # display.setFPS(30)

class ColorTwist(StaticObject.StaticObject):

    def __init__(self, colorList):
        super(ColorTwist, self).__init__()
        assert(len(colorList) >= 1)
        self.color = colorList[0]
        self.timeAsThisColor = 0
        self.colorList = colorList
        self.currentIndex = 0

    def draw(self, screen, offset=None):
        objectPosition = self.getPosition()
        if not offset is None:
            objectPosition[0] += offset[0]
            objectPosition[1] += offset[1]

        self._alignPosition(objectPosition)

        pygame.draw.circle(
            screen, self.color, (int(34 + objectPosition[0]), int(34 + objectPosition[1])), 100)

    def tick(self, delta):
        def lerp(vector1, vector2, scalarBetween0and1):
            def vecTimesScalar(vector, scalar):
                return [i * scalar for i in vector]

            def vecPlusVec(vector1, vector2):
                return [x + y for x, y in zip(vector1, vector2)]

            return vecPlusVec(vecTimesScalar(vector1, 1 - scalarBetween0and1), vecTimesScalar(vector2, scalarBetween0and1))

        def timeForStage(discreteStage):
            timeForEachStage = 0.21
            return discreteStage * timeForEachStage

        colorSeq = [(255, 0, 0), (255, 255, 0), (255, 0, 0),
                    (255, 0, 255), (255, 0, 0)]
        self.timeAsThisColor += delta
        if self.timeAsThisColor < timeForStage(1):
            self.color = lerp(colorSeq[0], colorSeq[
                1], (self.timeAsThisColor - timeForStage(0)) / (timeForStage(1) - timeForStage(0)))
        elif self.timeAsThisColor < timeForStage(2):
            self.color = lerp(colorSeq[1], colorSeq[
                2], (self.timeAsThisColor - timeForStage(1)) / (timeForStage(2) - timeForStage(1)))
        elif self.timeAsThisColor < timeForStage(3):
            self.color = lerp(colorSeq[2], colorSeq[
                3], (self.timeAsThisColor - timeForStage(2)) / (timeForStage(3) - timeForStage(2)))
        elif self.timeAsThisColor < timeForStage(4):
            self.color = lerp(colorSeq[3], colorSeq[
                4], (self.timeAsThisColor - timeForStage(3)) / (timeForStage(4) - timeForStage(3)))
        else:
            self.timeAsThisColor -= timeForStage(len(colorSeq) - 1)
            self.tick(0)


class ColorFlasher(StaticObject.StaticObject):

    def __init__(self, colorList):
        super(ColorFlasher, self).__init__()
        assert(len(colorList) >= 1)
        self.color = colorList[0]
        self.timeAsThisColor = 0
        self.colorList = colorList
        self.currentIndex = 0

    def draw(self, screen, offset=None):
        objectPosition = self.getPosition()
        if not offset is None:
            objectPosition[0] += offset[0]
            objectPosition[1] += offset[1]

        self._alignPosition(objectPosition)
        verts = [(0, 0), (0, 200), (200, 200), (200, 0)]
        pygame.draw.polygon(screen, self.color, map(lambda x: (
            x[0] + objectPosition[0], x[1] + objectPosition[1]), verts))

    def tick(self, delta):
        self.timeAsThisColor += delta
        secondsToBeColor = 0.3
        if self.timeAsThisColor >= secondsToBeColor:
            self.timeAsThisColor -= secondsToBeColor
            if self.currentIndex + 1 == len(self.colorList):
                self.currentIndex = 0
            else:
                self.currentIndex += 1

            self.color = self.colorList[self.currentIndex]

def main():
    init()
    hudRenderList = RenderList.RenderList("hud")
    playerRenderList = SortedRenderList.SortedRenderList("player")
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

    players = []

    def updatePlayers(event=None):
        numberOfPlayers = joysticks.updateJoysticks()
        if numberOfPlayers == 0:
            numberOfPlayers = 1
        while len(players):
            players[0].disable()
            players.pop(0)
        playerRenderList.removeAll()
        for i in range(0, numberOfPlayers):
            animatedGuy = AOPlayerCharacter.AOPlayerCharacter(i)
            animatedGuy.movePosition(i * 64 + 800, 730)
            playerRenderList.addObject(animatedGuy)
            players.append(animatedGuy)
    events.bindKeyDownEvent(["l"], updatePlayers)
    updatePlayers()

    tileMap = TileMap.TileMap("test1.json", 2)
    worldRenderList.addObject(tileMap)
    hihi = ColorFlasher([colors.BLUE, colors.RED, colors.GREEN])
    worldRenderList.addObject(hihi)
    woahWoah = ColorTwist(
        [colors.RED, colors.GREEN, colors.PURPLE, colors.TRANSPARENT])
    worldRenderList.addObject(woahWoah)

    def loadLevel1():
        tileMap.loadMap("default.json")
        updatePlayers()

    def loadLevel2():
        tileMap.loadMap("test1.json")
        updatePlayers()

    events.bindKeyDownEvent(["1"], lambda e: loadLevel1())
    events.bindKeyDownEvent(["2"], lambda e: loadLevel2())
    events.bindKeyDownEvent(["f"], lambda e: display.toggleFullscreen())
    events.bindKeyDownEvent(["g"], lambda e: display.decreaseScreenMode())
    events.bindKeyDownEvent(["h"], lambda e: display.increaseScreenMode())
    events.bindKeyDownEvent(["t"], lambda e: display.setSmallestResolution())
    events.bindKeyDownEvent(["y"], lambda e: display.setLargestResolution())
    events.bindKeyDownEvent(["o"], lambda e: sounds.playSoundOnce("startup"))
    while True:
        # Limit framerate to the desired FPS
        delta = clock.tick()

        # Handle game events through the event queue and tick all game
        # constructs
        events.handleEvents()
        events.tick(delta)

        mainCamera.centerOnObject(players[0])

        # Draw screen
        screen = display.getScreen()
        # screen.fill(colors.BLACK)
        worldRenderList.render(screen, mainCamera)
        playerRenderList.render(screen, mainCamera)
        particleRenderList.render(screen, mainCamera)
        hudRenderList.render(screen, hudCamera)
        pygame.display.update()

if __name__ == "__main__":
    main()
