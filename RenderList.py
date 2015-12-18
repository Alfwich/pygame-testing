import pygame

class RenderList():
    def __init__(self):
        self.objectIds = {}
        self.objects = []

    def addObject(self, obj):
        if not id(obj) in self.objectIds:
            self.objectIds[id(obj)] = True
            self.objects.append(obj)

    def renderList(self, screen):
        for obj in self.objects:
            screen.blit(obj.getBitmap(), obj.getPosition())
