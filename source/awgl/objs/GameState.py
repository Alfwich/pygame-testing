import QuadTree
from ..modules import events
import SortedRenderList, TileMap

class GameState(object):
    _globalGameState = None

    @staticmethod
    def setGlobalGameState(gameState):
        GameState._globalGameState = gameState

    @staticmethod
    def getGlobalGameState():
        return GameState._globalGameState

    def __init__(self):
        self._props = {}
        self._world = TileMap.TileMap()
        self._collider = None
        self._colliderObjects = []
        self._generatedObjects = set()
        self._generatedObjectsRenderList = SortedRenderList.SortedRenderList("gamestate-%d"%id(self))
        events.bindFrameEvent(self.updateCollider)

    def __getitem__(self, key):
        return self._props[key] if key in self._props else None

    def __setitem__(self, key, value):
        self._props[key] = value

    def setProperty(self, key, value):
        self._props[key] = value

    def getProperty(self, key):
        return self._props[key] if key in self._props else None

    @property
    def world(self):
        return self._world

    @world.setter
    def world(self, newWorld):
        self._world = newWorld

    @property
    def renderList(self):
        return self._generatedObjectsRenderList

    def loadMap(self, mapName):
        if self._world:
            if self._world.loadMap(mapName):
                for obj in list(self._generatedObjects):
                    self.disableObject(obj)
                self._colliderObjects = []
                self._generatedObjects = set()
                self._generatedObjectsRenderList.removeAll()

    def createGameObject(self, classType, **configuration):
        if self._world:
            newObject = classType(**configuration)
            if "location" in configuration:
                location = configuration["location"]
                newObject.position = (location[0]*self._world.tileWidth + self._world.tileWidth/2, location[1]*self._world.tileHeight + self._world.tileHeight/2)
            newObject.gameState = self
            newObject.bindEvents()
            newObject.begin()
            self._generatedObjects.add(newObject)
            self._generatedObjectsRenderList.add(newObject)
            return newObject
        else:
            print("Attempted to add object: %s, to uninitalized world" % str(classType))

    def registerCollidableObject(self, obj):
        if not obj in self._colliderObjects:
            self._colliderObjects.append(obj)

    def deregisterCollidableObject(self, obj):
        if obj in self._colliderObjects:
            self._colliderObjects.remove(obj)

    def disableObject(self, obj):
        obj.disabled = True
        self.deregisterCollidableObject(obj)
        if obj in self._generatedObjects:
            self._generatedObjects.remove(obj)

    def updateCollider(self):
        for obj in self._colliderObjects:
            obj.rect = obj.getRect()
        self._collider = QuadTree.QuadTree(self._colliderObjects)

    def getCollisions(self, rect, caller=None):
        collisions = self._collider.getHits(rect) if self._collider else []

        if caller in collisions:
            collisions.remove(caller)

        for obj in list(collisions):
            if True in [obj.hasCollided(caller), caller.hasCollided(obj) if caller else None]:
                collisions.remove(obj)

        return collisions
