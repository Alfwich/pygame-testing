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
        for y in range(0, self.getWidth(), self.tileWidth):
            for x in range(0, self.getHeight(), self.tileHeight):
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
        return self.map[y][x]

    def getTileAtWorldPosition(self, worldX, worldY):
        return self.getTileAtPosition(int(worldX/self.tileWidth), int(worldY/self.tileHeight))

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

        objectPosition[0] = int(objectPosition[0])
        objectPosition[1] = int(objectPosition[1])

        for rowIdx, row in enumerate(self.map):
            tileYPosition = objectPosition[1] + rowIdx * self.tileHeight
            if tileYPosition >= -self.tileHeight and tileYPosition < display.getScreenHeight():
                for colIdx, tile in enumerate(row):
                    tileXPosition = objectPosition[0] + colIdx * self.tileWidth
                    if tileXPosition >= -self.tileWidth and tileXPosition < display.getScreenWidth():
                        screen.blit(self.bitmap, (tileXPosition, tileYPosition), self.getTileRect(tile))
