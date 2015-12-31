import pygame, random
from ..awgl.modules import *
from ..awgl.objs import *

GUY_DIM = 64
animations.addAnimation("walking-guy-walk-left", [(GUY_DIM*i, GUY_DIM, GUY_DIM, GUY_DIM) for i in range(9)])
animations.addAnimation("walking-guy-walk-up", [(GUY_DIM*i, 0, GUY_DIM, GUY_DIM) for i in range(9)])
animations.addAnimation("walking-guy-walk-right", [(GUY_DIM*i, GUY_DIM*3, GUY_DIM, GUY_DIM) for i in range(9)])
animations.addAnimation("walking-guy-walk-down", [(GUY_DIM*i, GUY_DIM*2, GUY_DIM, GUY_DIM) for i in range(9)])

images.addToGlobalLoadList([
    ("walking-guy", "guy-walk.png")
])

class AOPlayerCharacter(AnimatedObject.AnimatedObject):
    def __init__(self, **configuration):
        super(AOPlayerCharacter, self).__init__()
        self.walkingSpeed = 125
        self.walkingFPS = 30
        self.currentSpeed = self.walkingSpeed
        self.maxFPS = self.walkingFPS
        self.velocity = [0,0]
        self.collisionOffset = [0, 10]
        self.collisionSize = [20, 25]
        self.playerId = configuration.get("player", 0)
        self.bitmap = images.getImage("walking-guy")
        self.setAnimation(animations.getAnimation("walking-guy-walk-left"))
        self.showPlayerTag()
        self.alignment = GameObject.alignment.BOTTOM_CENTER
        self.setNumberOfLoops(-1)
        self.setFrameRate(self.walkingFPS)
        self.play()

    def _getCollideObjects(self, rect):
        collidePlayers = self.gameState.getCollisions(rect, self)
        collidePlayers = set(map(lambda p: p.getRawRect(), collidePlayers))

        return collidePlayers

    def _getCollisionObjects(self, newPosition):
        selfRect = self.getRect()
        selfRect.x = newPosition[0]-self.collisionSize[0]/2
        selfRect.y = newPosition[1]-self.collisionSize[1]
        hits = self._getCollideObjects(selfRect) | self.gameState.world.getTilesOnRect(selfRect, "collision")
        return hits

    def _hasCollision(self, newPosition):
        return len(self._getCollisionObjects(newPosition)) > 1

    def _safeMoveAdjust(self, newPosition):
        collideObjectsX = self._getCollisionObjects((newPosition[0], self.position[1]))
        collideObjectsY = self._getCollisionObjects((self.position[0], newPosition[1]))

        if len(collideObjectsX) > 0:
            newPosition[0] = self.position[0]

        if len(collideObjectsY) > 0:
            newPosition[1] = self.position[1]

        return True

    def bindEvents(self):
        super(AOPlayerCharacter, self).bindEvents()
        self.addEvents([
            events.bindKeyAxis(["a", "K_LEFT"], ["d", "K_RIGHT"], self.moveLeft),
            events.bindKeyAxis(["w", "K_UP"], ["s", "K_DOWN"], self.moveUp),
            events.bindKeyDownEvent("6", self.changeColor),
            events.bindJoystickAxisMotionEvent(0, 0, self.moveLeft),
            events.bindJoystickAxisMotionEvent(0, 1, self.moveUp),
            events.bindJoystickButtonAxis(0, 1, 0, lambda e, v: self.modifyWalkingSpeed(v))
        ])


    def changeColor(self, event=None):
        self.tint = colors.randomColor()


    def begin(self):
        super(AOPlayerCharacter, self).begin()
        self.canCollide = True
        self.movePositionY(self.collisionSize[1]/2)

    def showPlayerTag(self):
        playerTagBG = Text.Text("P%d"%(self.playerId+1), None, colors.BLACK)
        playerTagBG.movePosition(-2, -self.height+2)
        self.addChild(playerTagBG)
        events.bindTimer(playerTagBG.disable, 3000)

        playerTag = Text.Text("P%d"%(self.playerId+1), None, colors.WHITE)
        playerTag.movePosition(0, -self.height)
        self.addChild(playerTag)
        events.bindTimer(playerTag.disable, 3000)

    def getRect(self):
        return pygame.Rect(self.positionX-self.collisionSize[0]/2, self.positionY-self.collisionSize[1], self.collisionSize[0], self.collisionSize[1])

    def moveLeft(self, e, value):
        self.velocity[0] = value

    def moveUp(self, e, value):
        self.velocity[1] = value

    def modifyWalkingSpeed(self, value):
        self.currentSpeed = self.walkingSpeed + 80 * value
        self.maxFPS = self.walkingFPS + 15 * value

    def updateMoveAnimation(self):
        if abs(self.velocity[0]) > abs(self.velocity[1]):
            self.setFrameRate(abs(self.velocity[0])*self.maxFPS)
            if self.velocity[0] > 0:
                self.setAnimation(animations.getAnimation("walking-guy-walk-right"))
            else:
                self.setAnimation(animations.getAnimation("walking-guy-walk-left"))
        else:
            self.setFrameRate(abs(self.velocity[1])*self.maxFPS)
            if self.velocity[1] > 0:
                self.setAnimation(animations.getAnimation("walking-guy-walk-down"))
            else:
                self.setAnimation(animations.getAnimation("walking-guy-walk-up"))

    def tick(self, delta):
        super(AOPlayerCharacter, self).tick(delta)
        if self.gameState["currentPlayerIndex"] == self.playerId:
            if not self.velocity[0] == 0 or not self.velocity[1] == 0:
                self.updateMoveAnimation()
                newPosition = [self.rawPosition[0] + self.velocity[0] * self.currentSpeed * delta, self.rawPosition[1] + self.velocity[1] * self.currentSpeed * delta]
                if self._safeMoveAdjust(newPosition):
                    self.position = (newPosition[0], newPosition[1])
            else:
                self.setFrame(0)
                self.setFrameRate(0)
        else:
            self.setFrame(0)
            self.setFrameRate(0)
