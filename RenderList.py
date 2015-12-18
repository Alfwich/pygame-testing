import pygame

class RenderList():
    def __init__(self):
        self.objectIds = {}
        self.objects = []

    def addObject(self, obj):
        if not id(obj) in self.objectIds:
            self.objectIds[id(obj)] = True
            self.objects.append(obj)

    def removeObject(self, removeObj):
        if id(removeObj) in self.objectIds:
            self.objectIds.pop(id(remove))
            for idx, obj in enumerate(self.objects):
                if obj is removeObj:
                    self.objects[idx] = None
                    break
            self.objects = filter(lambda y: y, self.objects)

    def renderList(self, screen, camera=None):
        for obj in self.objects:
            objectBitmap = obj.getBitmap()
            objectPosition = camera.transformPosition(obj.getPosition()) if not camera is None else obj.getPosition()
            objectRenderRect = obj.getRenderRect()
            screen.blit(objectBitmap, objectPosition, objectRenderRect)
