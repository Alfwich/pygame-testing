import pygame
from ..modules import images, display
import StaticObject

DEFAULT_MAP_TEMPLATE = "data/map/%s"

class TileMap(StaticObject.StaticObject):
    def __init__(self, tileSurface, tileWidth, tileHeight):
        super(TileMap, self).__init__()
        self.tiles = []
        self.setBitmap(tileSurface)
        self.tileWidth = tileWidth
        self.tileHeight = tileHeight
        self.map = None
        self.disableTick()


    def setupDefaultTiles(self):
        for x in range(0, self.getWidth(), self.tileWidth):
            for y in range(0, self.getWidth(), self.tileWidth):
                self.addTileRect(x, y)

    def scaleTiles(self, xScale, yScale):
        self.scaleBitmap(xScale, yScale)
        self.tileWidth = self.tileWidth * int(xScale)
        self.tileHeight = self.tileHeight * int(yScale)
        self.tiles = []

    def addTileRect(self, x, y):
        self.tiles.append(pygame.Rect(x, y, self.tileWidth, self.tileHeight))

    def getTileRect(self, tileIndex):
        return self.tiles[tileIndex]

    def getTileAtPosition(self, x, y):
        return 0

    def loadMap(self, filePath):
        with open(DEFAULT_MAP_TEMPLATE%filePath, "r") as f:
            self.map = []
            for line in f:
                self.map.append([])
                for col in line.strip().split(","):
                    self.map[-1].append(int(col))

    def draw(self, screen, offset=None):
        objectPosition = self.getPosition()
        if not offset is None:
            objectPosition[0] += offset[0]
            objectPosition[1] += offset[1]

        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                tilePosition = (objectPosition[0] + y * self.tileWidth, objectPosition[1] + x * self.tileHeight)
                if tilePosition[0] >= 0 and tilePosition[0] < display.getScreenWidth() and tilePosition[1] >= 0 and tilePosition[1] < display.getScreenHeight():
                    screen.blit(self.bitmap, tilePosition, self.getTileRect(self.map[x][y]))
