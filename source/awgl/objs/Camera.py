
class Camera():
    def __init__(self):
        self.offset = [0, 0]

    def transformWorldPosition(self, position):
        position[0] += self.offset[0]
        position[1] += self.offset[1]

    def transformScreenPosition(self, position):
        position[0] -= self.offset[0]
        position[1] -= self.offset[1]

    def setOffset(self, x, y):
        self.offset = [x, y]

    def getOffset(self):
        return list(self.offset)

    def moveOffset(self, deltaX, deltaY):
        self.offset[0] += deltaX
        self.offset[1] += deltaY
