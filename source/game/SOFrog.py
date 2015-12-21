import pygame, random
from ..awgl.objs import *
from ..awgl.modules import *

images.addToGlobalLoadList([
    ("frog", "frog-face.png"),
    ("frog2", "funny-frog-face.png")
])

class SOFrog(StaticObject.StaticObject):
    def __init__(self):
        super(SOFrog, self).__init__()
        self.setBitmap(images.getImage("frog"))
        self.moveSpeed = random.randint(50,100)
        events.bindKeyAxis(["w","K_UP"], ["s", "K_DOWN"], self.moveUp)
        events.bindKeyAxis(["a", "K_LEFT"], ["d","K_RIGHT"], self.moveRight)
        events.bindKeyDownEvent("o", lambda e: self.setBitmap(images.getImage("frog")))
        events.bindKeyDownEvent("p", lambda e: self.setBitmap(images.getImage("frog2")))

    def moveUp(self, event, value):
        self.velocity[1] = self.moveSpeed * value

    def moveRight(self, event, value):
        self.velocity[0] = self.moveSpeed * value

    def tick(self, delta):
       super(SOFrog, self).tick(delta)
       if not self.velocity[0] == 0 or not self.velocity[1] == 0:
           self.position[0] += self.velocity[0] * delta
           self.position[1] += self.velocity[1] * delta
