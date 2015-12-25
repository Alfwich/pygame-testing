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
    playerCharacters = []

    @staticmethod
    def clearPlayerCharacters():
        AOPlayerCharacter.playerCharacters = []

    def __init__(self, controllerId=0, gameState=None):
        super(AOPlayerCharacter, self).__init__()
        self.walkingSpeed = random.randint(100, 150)
        self.walkingFPS = 30
        self.currentSpeed = self.walkingSpeed
        self.maxFPS = self.walkingFPS
        self.gameState = gameState
        self.setBitmap(images.getImage("walking-guy"))
        self.setAnimation(animations.getAnimation("walking-guy-walk-left"))
        self.setAlignmentY(GameObject.alignment.BOTTOM)
        self.setNumberOfLoops(-1)
        self.setFrameRate(self.walkingFPS)
        self.velocity = [0,0]
        self.collisionSize = [20, 20]
        self.play()

        gameWorld = gameState.getMap()
        if not gameWorld is None:
            while True:
                spawnLocation = list(random.choice(gameWorld.getTiles("spawn")).position)
                spawnLocation[0] = (spawnLocation[0]*gameWorld.getTileWidth()) + gameWorld.getTileWidth()/2
                spawnLocation[1] = (spawnLocation[1]*gameWorld.getTileHeight()) + gameWorld.getTileHeight()/2
                self.setPosition(spawnLocation[0], spawnLocation[1])
                if not self._hasCollision(self.position):
                    break

        if controllerId == 0:
            self.addEvents([
                events.bindKeyAxis("i", "l", self.moveRight),
                events.bindKeyAxis("k", "o", self.moveDown)
            ])

        controllerId = 0
        self.addEvents([
            events.bindJoystickAxisMotionEvent(controllerId, 0, self.moveRight),
            events.bindJoystickAxisMotionEvent(controllerId, 1, self.moveDown),
            events.bindJoystickButtonAxis(controllerId, 1, 0, lambda e, v: self.modifyWalkingSpeed(v))
        ])

        playerTagBG = Text.Text("P%d"%(controllerId+1), None, colors.BLACK)
        playerTagBG.movePosition(-2, -(self.getHeight())+2)
        self.children.append(playerTagBG)
        events.bindTimer(playerTagBG.disable, 3000)

        playerTag = Text.Text("P%d"%(controllerId+1), None, colors.WHITE)
        playerTag.movePosition(0, -(self.getHeight()))
        self.children.append(playerTag)
        events.bindTimer(playerTag.disable, 3000)

        collRect = StaticObject.StaticObject()
        collRectSurface = pygame.Surface(self.collisionSize)
        collRectSurface.fill(colors.RED)
        collRect.setBitmap(collRectSurface)
        #self.children.append(collRect)

        AOPlayerCharacter.playerCharacters.append(self)

    def _hasCollision(self, newPosition):
        selfRect = pygame.Rect(newPosition[0]-self.collisionSize[0], newPosition[1]-self.collisionSize[1]/2, self.collisionSize[0], self.collisionSize[1])
        for player in AOPlayerCharacter.playerCharacters:
            if not player is self:
                otherRect = pygame.Rect(player.getPositionX()-player.collisionSize[0]/2, player.getPositionY()-player.collisionSize[1]/2, player.collisionSize[0], player.collisionSize[1])
                if selfRect.colliderect(otherRect):
                    return True


    def moveRight(self, e, value):
        self.velocity[0] = value

    def moveDown(self, e, value):
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
        if not self.velocity[0] == 0 or not self.velocity[1] == 0:
            self.updateMoveAnimation()
            if not self.velocity[0] == 0:
                deltaX = self.velocity[0] * delta * self.currentSpeed
                self.position[0] += deltaX
                sign = 1 if deltaX > 0 else -1
                if len(self.gameState.getMap().getTilesAtPosition(self.position[0] + self.collisionSize[0] * sign, self.position[1], "collision")) > 0 or self._hasCollision(self.position):
                    self.position[0] -= deltaX

            if not self.velocity[1] == 0:
                deltaY = self.velocity[1] * delta * self.currentSpeed
                sign = 1 if deltaY > 0 else -1
                self.position[1] += deltaY
                if len(self.gameState.getMap().getTilesAtPosition(self.position[0], self.position[1] + self.collisionSize[1] * sign, "collision")) > 0 or self._hasCollision(self.position):
                    self.position[1] -= deltaY
        else:
            self.setFrame(0)
            self.setFrameRate(0)
