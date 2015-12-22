import pygame

class RenderList(object):
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
            self.objectIds.pop(id(removeObj))
            for idx, obj in enumerate(self.objects):
                if obj is removeObj:
                    self.objects[idx] = None
                    break
            self.objects = filter(lambda y: y, self.objects)

    def removeAll(self):
        self.objects = []
        self.objectIds = {}

    def render(self, screen, camera=None):
        shouldCameraTransform = not camera is None
        for obj in self.objects:
            obj.render(screen, camera)
