
class Camera():
    def __init__(self):
        self.offset = [0, 0]
        self.locked = False

    def transformWorldPosition(self, position):
        return [position[0] + self.offset[0], position[1] + self.offset[1]]

    def transformScreenPosition(self, position):
        return [position[0] - self.offset[0], position[1] - self.offset[1]]

    def setOffset(self, x, y):
        if not self.locked:
            self.offset = [x, y]

    def moveOffset(self, deltaX, deltaY):
        if not self.locked:
            self.offset[0] += deltaX
            self.offset[1] += deltaY

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False
