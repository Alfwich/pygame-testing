import pygame

class RenderList():
    lists = {}

    def getList(name):
        if name in RenderList.lists:
            return RenderList[name]
        return None

    def __init__(self, name):
        self.objectIds = {}
        self.objects = []
        RenderList.lists[name] = self

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

    def render(self, screen, camera=None):
        shouldCameraTransform = not camera is None
        for obj in self.objects:
            if obj._isValid:
                objectBitmap = obj.getBitmap()
                objectPosition = obj.getPosition()
                objectRenderRect = obj.getRenderRect()

                if shouldCameraTransform:
                    objectPosition = camera.transformWorldPosition(objectPosition)

                screen.blit(objectBitmap, objectPosition, objectRenderRect)
