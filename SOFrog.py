import pygame, StaticObject as SO, images, events


images.addToGlobalLoadList([
    ("frog", "frog-face.png"),
    ("frog2", "funny-frog-face.png")
])

class SOFrog(SO.StaticObject):
    def __init__(self):
        super(SOFrog, self).__init__()
        self.setBitmap(images.getImage("frog"))
        self.moveSpeed = 100
        events.bindKeyDownEvent(["w","a","s","d"], self.moveKeyDown)
        events.bindKeyUpEvent(["w","a","s","d"], self.moveKeyUp)
        events.bindKeyDownEvent(["o", "p"], self.changeFaceKeyDown)

    def moveKeyDown(self, event):
        if event.unicode == u"w":
            self.velocity[1] = -self.moveSpeed
        elif event.unicode == u"s":
            self.velocity[1] = self.moveSpeed
        elif event.unicode == u"a":
            self.velocity[0] = -self.moveSpeed
        elif event.unicode == u"d":
            self.velocity[0] = self.moveSpeed

    def moveKeyUp(self, event):
        if event.key in [ord("w"), ord("s")]:
            self.velocity[1] = 0
        elif event.key in [ord("a"), ord("d")]:
            self.velocity[0] = 0

    def changeFaceKeyDown(self, event):
        if event.unicode == u"o":
            self.setBitmap(images.getImage("frog"))
        elif event.unicode == u"p":
            self.setBitmap(images.getImage("frog2"))

    def tick(self, delta):
       super(SOFrog, self).tick(delta)
       if not self.velocity[0] == 0 or not self.velocity[1] == 0:
           self.position[0] += self.velocity[0] * delta
           self.position[1] += self.velocity[1] * delta
