import pygame, json, zlib, base64
from ..modules import images, display, colors
import StaticObject, TileSet

DEFAULT_MAP_TEMPLATE = "data/map/%s"

class TileMap(StaticObject.StaticObject):
    def __init__(self, mapFile, globalScale=1):
        super(TileMap, self).__init__()
        self.map = {}
        self.tileSets = []
        self.cachedMapSurfaces = {}
        self.globalScale = globalScale
        self.disableTick()
        self.loadMap(mapFile)

    def _clearTileMap(self):
        self.map = {}
        self.tileSets = []
        self.cachedMapSurfaces = {}

    def _setupCachedSurface(self, layerId):
        tileLayer = self.map[layerId]
        tileSetBase = self.tileSets[0]
        self.cachedMapSurfaces[layerId] = pygame.Surface((len(tileLayer[0])*tileSetBase.getTileWidth(), len(tileLayer)*tileSetBase.getTileHeight()), pygame.SRCALPHA, 32)
        self.cachedMapSurfaces[layerId] = self.cachedMapSurfaces[layerId].convert_alpha()
        """
        self.cachedMapSurfaces[layerId].set_colorkey((255,0,255))
        self.cachedMapSurfaces[layerId].fill(colors.TRANSPARENT)
        """
        for rowIdx, row in enumerate(tileLayer):
            tileYPosition = rowIdx * tileSetBase.getTileHeight()
            for colIdx, tile in enumerate(row):
                tileXPosition = colIdx * tileSetBase.getTileWidth()
                if not tile == 0:
                    self.cachedMapSurfaces[layerId].blit(self._getTileBitmap(tile), (tileXPosition, tileYPosition), self._getTileRect(tile))

    def _decodeMapLayerData(self, data):
        FLIPPED_HORIZONTALLY_FLAG = 0x80000000
        FLIPPED_VERTICALLY_FLAG   = 0x40000000
        FLIPPED_DIAGONALLY_FLAG   = 0x20000000

        byteArray = bytearray(data.decode("base64").decode("zlib"))
        mapData = [byteArray[i] | byteArray[i+1] << 8 | byteArray[i+2] << 16 | byteArray[i+3] << 24 for i in range(0, len(byteArray), 4)]
        mapData = map(lambda v: int(v & (~(FLIPPED_DIAGONALLY_FLAG|FLIPPED_VERTICALLY_FLAG|FLIPPED_HORIZONTALLY_FLAG))), mapData)
        return mapData

    def _loadMapLayer(self, layer, layerId=0):
        layerData = self._decodeMapLayerData(layer["data"])
        self.map[layerId] = []
        for x in range(0, layer["width"]):
            self.map[layerId].append([])
            for y in range(0, layer["height"]):
                self.map[layerId][-1].append(layerData.pop(0))
        self._setupCachedSurface(layerId)

    def _getCorrectTileSet(self, tileIndex):
        index = len(self.tileSets)-1

        while not self.tileSets[index].tileIndexIsMember(tileIndex):
            index -= 1

        return self.tileSets[index]

    def _getTileBitmap(self, tileIndex):
        tileSet = self._getCorrectTileSet(tileIndex)
        return tileSet.getBitmap() if not tileSet is None else None

    def _getTileRect(self, tileIndex):
        tileSet = self._getCorrectTileSet(tileIndex)
        return tileSet.getTileRect(tileIndex) if not tileSet is None else None

    def getTileAtPosition(self, x, y):
        return self.map[y][x]

    def getTileAtWorldPosition(self, worldX, worldY):
        return self.getTileAtPosition(int(worldX/self.tileWidth), int(worldY/self.tileHeight))

    def loadMap(self, filePath):
        with open(DEFAULT_MAP_TEMPLATE%filePath, "r") as f:
            self._clearTileMap()
            cfg = json.load(f)
            for tileSet in cfg["tilesets"]:
                tileSetImage = images.loadImage("%s-tile-set-%s" % (filePath, tileSet["image"]), tileSet["image"].split("/")[-1])
                tileSize = tileSet["tilewidth"]
                tileIndexes = (int(tileSet["firstgid"]), int(tileSet["tilecount"])+int(tileSet["firstgid"]))
                scaleModifier = int(tileSet["properties"]["scale"]) if "scale" in tileSet["properties"] else self.globalScale
                self.tileSets.append(TileSet.TileSet(tileSetImage, tileSize, tileIndexes, scaleModifier))
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
