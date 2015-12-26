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
    playerCharactersQuadTree = QuadTree.QuadTree([])

    @staticmethod
    def setupQuadTree():
        for player in AOPlayerCharacter.playerCharacters:
            player.rect = player.getRect()

        AOPlayerCharacter.playerCharactersQuadTree = QuadTree.QuadTree(AOPlayerCharacter.playerCharacters)

    @staticmethod
    def getCollideObjects(rect):
        return AOPlayerCharacter.playerCharactersQuadTree.hit(rect) if not AOPlayerCharacter.playerCharactersQuadTree is None else []

    @staticmethod
    def clearPlayerCharacters():
        AOPlayerCharacter.playerCharacters = []

    def __init__(self, controllerId=0, gameState=None, spawnLocation=(0,0)):
        super(AOPlayerCharacter, self).__init__()
        self.walkingSpeed = random.randint(100, 150)
        self.walkingFPS = 30
        self.currentSpeed = self.walkingSpeed
        self.maxFPS = self.walkingFPS
        self.gameState = gameState
        self.velocity = [0,0]
        self.collisionSize = [20, 20]
        self.rect = None
        self.setBitmap(images.getImage("walking-guy"))
        self.setAnimation(animations.getAnimation("walking-guy-walk-left"))
        self.setAlignmentY(GameObject.alignment.BOTTOM)
        self.setNumberOfLoops(-1)
        self.setFrameRate(self.walkingFPS)
        self.setPosition(spawnLocation[0]*32+20, spawnLocation[1]*32+20)
        self.play()

        if controllerId == 0:
            self.addEvents([
                events.bindKeyAxis("a", "d", self.moveLeft),
                events.bindKeyAxis("w", "s", self.moveUp)
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

        controllerId = 0
        self.addEvents([
            events.bindJoystickAxisMotionEvent(controllerId, 0, self.moveLeft),
            events.bindJoystickAxisMotionEvent(controllerId, 1, self.moveUp),
            events.bindJoystickButtonAxis(controllerId, 1, 0, lambda e, v: self.modifyWalkingSpeed(v))
        ])

        AOPlayerCharacter.playerCharacters.append(self)

    def _hasCollision(self, newPosition):
        selfRect = pygame.Rect(newPosition[0]-self.collisionSize[0]/2, newPosition[1]-self.collisionSize[1]/2, self.collisionSize[0], self.collisionSize[1])
        hits = AOPlayerCharacter.getCollideObjects(selfRect) | self.gameState.getMap().getTilesOnRect(selfRect, "collision")
        return len(hits) > 1
        """
        for player in AOPlayerCharacter.playerCharacters:
            if not player is self:
                otherRect = pygame.Rect(player.getPositionX()-player.collisionSize[0]/2, player.getPositionY()-player.collisionSize[1]/2, player.collisionSize[0], player.collisionSize[1])
                if selfRect.colliderect(otherRect):
                    return True
        """
    def getRect(self):
        return pygame.Rect(self.getPositionX()-self.collisionSize[0]/2, self.getPositionY()-self.collisionSize[1]/2, self.collisionSize[0], self.collisionSize[1])

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
        if not self.velocity[0] == 0 or not self.velocity[1] == 0:
            self.updateMoveAnimation()
            if not self.velocity[0] == 0:
                deltaX = self.velocity[0] * delta * self.currentSpeed
                self.position[0] += deltaX
                if self._hasCollision(self.position):
                    self.position[0] -= deltaX

            if not self.velocity[1] == 0:
                deltaY = self.velocity[1] * delta * self.currentSpeed
                self.position[1] += deltaY
                if self._hasCollision(self.position):
                    self.position[1] -= deltaY
        else:
            self.setFrame(0)
            self.setFrameRate(0)
