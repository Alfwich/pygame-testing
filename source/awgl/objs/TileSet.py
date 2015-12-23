import pygame


class TileSet(object):
    def __init__(self, bitmap, tileSize, tileIndexes=None, scale=1):
        if tileIndexes is None:
            tileIndexes = (1,256)
        self._bitmap = bitmap
        self.bitmap = bitmap
        self.tileSize = [tileSize, tileSize]
        self.tileIndexes = tileIndexes
        self.tiles = []
        if not scale == 1:
            self.scaleSet(scale)
        else:
            self._setupDefaultTiles()

    def _addTileRect(self, x, y):
        self.tiles.append(pygame.Rect(x, y, self.tileSize[0], self.tileSize[1]))

    def _setupDefaultTiles(self):
        self.tiles = []
        for y in range(0, self.bitmap.get_width(), self.tileSize[0]):
            for x in range(0, self.bitmap.get_height(), self.tileSize[1]):
                self._addTileRect(x, y)

    def getBitmap(self):
        return self.bitmap

    def scaleSet(self, scale):
        if not scale == 1:
            self.bitmap = pygame.transform.scale(self._bitmap, (int(self._bitmap.get_width()*scale), int(self._bitmap.get_height()*scale)))
            self.tileSize = map(lambda x: x*scale, self.tileSize)
            self._setupDefaultTiles()

    def getTileRect(self, tileIndex):
        return self.tiles[tileIndex-self.tileIndexes[0]]

    def tileIndexIsMember(self, tileIndex):
        return tileIndex >= self.tileIndexes[0] and tileIndex <= self.tileIndexes[1]

    def getTileWidth(self):
        return self.tileSize[0]

    def getTileHeight(self):
        return self.tileSize[1]
