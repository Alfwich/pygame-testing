import QuadTree
from ..modules import events

class GameState(object):
    def __init__(self):
        self.props = {}
        self.tileMap = None
        self.collider = None
        self.colliderObjects = []
        self.generatedObjects = set()
        events.bindFrameEvent(self.updateCollider)

    def setMap(self, newMap):
        self.tileMap = newMap

    def getMap(self):
        return self.tileMap

    def registerCollidableObject(self, obj):
        if not obj in self.colliderObjects:
            self.colliderObjects.append(obj)

    def deregisterCollidableObject(self, obj):
        if obj in self.colliderObjects:
            self.colliderObjects.remove(obj)

    def updateCollider(self):
        for obj in self.colliderObjects:
            obj.rect = obj.getRect()
        self.collider = QuadTree.QuadTree(self.colliderObjects)

    def getCollisions(self, rect, caller=None):
        collisions = self.collider.getHits(rect) if self.collider else []

        if caller in collisions:
            collisions.remove(caller)

        for obj in list(collisions):
            if True in [obj.hasCollided(caller), caller.hasCollided(obj) if caller else None]:
                collisions.remove(obj)

        return collisions

    def setProperty(self, key, value):
        self.props[key] = value

    def getProperty(self, key):
        return self.props[key] if key in self.props else None
