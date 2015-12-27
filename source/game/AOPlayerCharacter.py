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
    def __init__(self, controllerId=0, gameState=None, spawnLocation=(0, 0)):
        super(AOPlayerCharacter, self).__init__()
        self.walkingSpeed = 125
        self.walkingFPS = 30
        self.currentSpeed = self.walkingSpeed
        self.maxFPS = self.walkingFPS
        self.velocity = [0,0]
        self.collisionOffset = [0, 10]
        self.collisionSize = [20, 25]
        self.playerId = controllerId
        self.setGameState(gameState)
        self.setBitmap(images.getImage("walking-guy"))
        self.setAnimation(animations.getAnimation("walking-guy-walk-left"))
        self.showPlayerTag()
        self.setAlignmentY(GameObject.alignment.BOTTOM)
        self.setNumberOfLoops(-1)
        self.setFrameRate(self.walkingFPS)
        self.play()

        gameWorld = gameState.getMap()
        self.setPosition(spawnLocation[0]*gameWorld.getTileWidth()+16, spawnLocation[1]*gameWorld.getTileHeight() + 16 + self.collisionSize[1]/2)

        if controllerId == 0:
            self.addEvents([
                events.bindKeyAxis("a", "d", self.moveLeft),
                events.bindKeyAxis("w", "s", self.moveUp)
            ])

        controllerId = 0
        self.addEvents([
            events.bindJoystickAxisMotionEvent(controllerId, 0, self.moveLeft),
            events.bindJoystickAxisMotionEvent(controllerId, 1, self.moveUp),
            events.bindJoystickButtonAxis(controllerId, 1, 0, lambda e, v: self.modifyWalkingSpeed(v))
        ])

        gameState.registerCollidableObject(self)

    def _getCollideObjects(self, rect):
        collidePlayers = self.getGameState().getCollisions(rect, self)
        collidePlayers = set(map(lambda p: p.getRawRect(), collidePlayers))

        return collidePlayers

    def _getCollisionObjects(self, newPosition):
        selfRect = self.getRect()
        selfRect.x = newPosition[0]-self.collisionSize[0]/2
        selfRect.y = newPosition[1]-self.collisionSize[1]
        hits = self._getCollideObjects(selfRect) | self.getGameState().getMap().getTilesOnRect(selfRect, "collision")
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

    def showPlayerTag(self):
        playerTagBG = Text.Text("P%d"%(self.playerId+1), None, colors.BLACK)
        playerTagBG.movePosition(-2, -(self.getHeight())+2)
        self.children.append(playerTagBG)
        events.bindTimer(playerTagBG.disable, 3000)

        playerTag = Text.Text("P%d"%(self.playerId+1), None, colors.WHITE)
        playerTag.movePosition(0, -(self.getHeight()))
        self.children.append(playerTag)
        events.bindTimer(playerTag.disable, 3000)

    def getRect(self):
        return pygame.Rect(self.getPositionX()-self.collisionSize[0]/2, self.getPositionY()-self.collisionSize[1], self.collisionSize[0], self.collisionSize[1])

    def moveLeft(self, e, value):
        self.velocity[0] = value

    def moveUp(self, e, value):
        self.velocity[1] = value

    def modifyWalkingSpeed(self, value):
        self.currentSpeed = self.walkingSpeed + 80 * value
        self.maxFPS = self.walkingFPS + 15 * value

    def hasCollided(self, other):
        if other and other.hasTag("powerup"):
            other.disable()
            return True

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
        if not self.velocity[0] == 0 or not self.velocity[1] == 0:
            self.updateMoveAnimation()
            newPosition = [self.position[0] + self.velocity[0] * self.currentSpeed * delta, self.position[1] + self.velocity[1] * self.currentSpeed * delta]
            if self._safeMoveAdjust(newPosition):
                self.setPosition(newPosition[0], newPosition[1])
        else:
            self.setFrame(0)
            self.setFrameRate(0)
