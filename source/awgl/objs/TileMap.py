import pygame, json, zlib, base64
from ..modules import images, display, colors
import StaticObject

DEFAULT_MAP_TEMPLATE = "data/map/%s"

class TileMap(StaticObject.StaticObject):
    def __init__(self, tileSurface, tileWidth, tileHeight):
        super(TileMap, self).__init__()
        self.tiles = []
        self.setBitmap(tileSurface)
        self.tileWidth = tileWidth
        self.tileHeight = tileHeight
        self.blockingTiles = []
        self.map = {}
        self.cachedMapSurfaces = {}
        self.disableTick()


    def _setupCachedSurface(self, layerId):
        tileLayer = self.map[layerId]
        self.cachedMapSurfaces[layerId] = pygame.Surface((len(tileLayer[0])*self.tileWidth, len(tileLayer)*self.tileHeight), pygame.SRCALPHA, 32)
        self.cachedMapSurfaces[layerId] = self.cachedMapSurfaces[layerId].convert_alpha()
        """
        self.cachedMapSurfaces[layerId].set_colorkey((255,0,255))
        self.cachedMapSurfaces[layerId].fill(colors.TRANSPARENT)
        """
        for rowIdx, row in enumerate(tileLayer):
            tileYPosition = rowIdx * self.tileHeight
            for colIdx, tile in enumerate(row):
                tileXPosition = colIdx * self.tileWidth
                if not tile == -1:
                    self.cachedMapSurfaces[layerId].blit(self.bitmap, (tileXPosition, tileYPosition), self.getTileRect(tile))

    def _decodeMapLayerData(self, data):
        FLIPPED_HORIZONTALLY_FLAG = 0x80000000
        FLIPPED_VERTICALLY_FLAG   = 0x40000000
        FLIPPED_DIAGONALLY_FLAG   = 0x20000000

        byteArray = bytearray(data.decode("base64").decode("zlib"))
        mapData = [byteArray[i] | byteArray[i+1] << 8 | byteArray[i+2] << 16 | byteArray[i+3] << 24 for i in range(0, len(byteArray), 4)]
        mapData = map(lambda v: int(v & (~(FLIPPED_DIAGONALLY_FLAG|FLIPPED_VERTICALLY_FLAG|FLIPPED_HORIZONTALLY_FLAG)))-1, mapData)
        return mapData

    def _loadMapLayer(self, layer, layerId=0):
        layerData = self._decodeMapLayerData(layer["data"])
        self.map[layerId] = []
        for x in range(0, layer["width"]):
            self.map[layerId].append([])
            for x in range(0, layer["height"]):
                self.map[layerId][-1].append(layerData.pop(0))
        self._setupCachedSurface(layerId)

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
            cfg = json.load(f)
            for idx, layer in enumerate(cfg["layers"]):
                self._loadMapLayer(layer, idx)

    def draw(self, screen, offset=None):
        objectPosition = self.getPosition()
        if not offset is None:
            objectPosition[0] += offset[0]
            objectPosition[1] += offset[1]

        objectPosition[0] = int(objectPosition[0])
        objectPosition[1] = int(objectPosition[1])

        for layer, tileLayer in self.map.iteritems():
            renderRect = pygame.Rect(-objectPosition[0], -objectPosition[1], display.getScreenWidth(), display.getScreenHeight())
            screen.blit(self.cachedMapSurfaces[layer], (0, 0), renderRect)
            """
            for rowIdx, row in enumerate(tileLayer):
                tileYPosition = objectPosition[1] + rowIdx * self.tileHeight
                if tileYPosition >= -self.tileHeight and tileYPosition < display.getScreenHeight():
                    for colIdx, tile in enumerate(row):
                        tileXPosition = objectPosition[0] + colIdx * self.tileWidth
                        if not tile == -1 and tileXPosition >= -self.tileWidth and tileXPosition < display.getScreenWidth():
            """
