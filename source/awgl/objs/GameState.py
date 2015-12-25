

class GameState(object):
    def __init__(self):
        self.props = {}
        self.tileMap = None

    def setMap(self, newMap):
        self.tileMap = newMap

    def getMap(self):
        return self.tileMap

    def setProperty(self, key, value):
        self.props[key] = value

    def getProperty(self, key):
        return self.props[key] if key in self.props else None
