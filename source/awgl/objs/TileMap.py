import pygame, json, zlib, base64, sys
from ..modules import images, display, colors
import StaticObject, TileSet, QuadTree

DEFAULT_MAP_TEMPLATE = "data/map/%s"

class TileMap(StaticObject.StaticObject):
    class Tile():
        def __init__(self, rect, value):
            self.rect = rect
            self.value = value

    class MapLayer():
        def __init__(self, rawLayerData):
            self.map = []
            self.layerData = rawLayerData
            self.cachedLayer = None
            self._initMapWithLayerData()

        def __getitem__(self, a):
            return self.map[a]

        def _initMapWithLayerData(self):
            self.map = []
            data = self._decodeMapLayerData()
            if not data is None:
                for x in range(0, self.layerData["width"]):
                    self.map.append([])
                    for y in range(0, self.layerData["height"]):
                        self.map[-1].append(data.pop(0))


        def _decodeMapLayerData(self):
            FLIPPED_HORIZONTALLY_FLAG = 0x80000000
            FLIPPED_VERTICALLY_FLAG   = 0x40000000
            FLIPPED_DIAGONALLY_FLAG   = 0x20000000

            encodeType = str(self.layerData["encoding"])
            compressionType = str(self.layerData["compression"])
            try:
                byteArray = bytearray(self.layerData["data"].decode(encodeType).decode(compressionType))
                mapData = [byteArray[i] | byteArray[i+1] << 8 | byteArray[i+2] << 16 | byteArray[i+3] << 24 for i in range(0, len(byteArray), 4)]
                mapData = map(lambda v: int(v & (~(FLIPPED_DIAGONALLY_FLAG|FLIPPED_VERTICALLY_FLAG|FLIPPED_HORIZONTALLY_FLAG))), mapData)
            except Exception:
                print("Could not extract map layer data for layers: %s (%s)" % (self.layerData["name"], sys.exc_info()[0]))
                self.layerData["visible"] = False
                return None

            return mapData

        def isVisible(self):
            return self.layerData["visible"]

        def getName(self):
            return self.layerData["name"]

        def getWidth(self):
            return int(self.layerData["width"])

        def getHeight(self):
            return int(self.layerData["height"])

    def __init__(self, mapFile, globalScale=1):
        super(TileMap, self).__init__()
        self.mapLayers = {}
        self.mapLayerTypes = {}
        self.tileSets = []
        self.cachedLayerRenderObject = {}
        self.globalScale = globalScale
        self.disableTick()
        self.loadMap(mapFile)

    def _clearTileMap(self):
        self.mapLayers = {}
        self.mapLayerTypes = {}
        self.tileSets = []
        self.cachedLayerRenderObject = {}

    def _createCachedSurface(self, tileLayer):
        newSurface = pygame.Surface((len(tileLayer[0])*self.tileSets[0].getTileWidth(), len(tileLayer)*self.tileSets[0].getTileHeight()), pygame.SRCALPHA, 32)
        return newSurface.convert_alpha()
        """
        self.cachedMapSurfaces[layerId].set_colorkey((255,0,255))
        self.cachedMapSurfaces[layerId].fill(colors.TRANSPARENT)
        """
    def _mapFilledPercentage(self, layer):
        filled = sum([sum(map(lambda y: 0 if y == 0 else 1,x)) for x in layer])
        size = sum([sum([1 for y in x ]) for x in layer])
        return filled/float(size)

    def _shouldSurfaceCache(self, layerId):
        return True
        """ Needs more thought
        tileLayer = self.mapLayers[layerId].map
        if self._mapFilledPercentage(tileLayer) > 0.25:
            return True
        return False
        """

    def _setupCachedLayer(self, layerId):
        if self._shouldSurfaceCache(layerId):
            self._setupCachedSurface(layerId)
        else:
            self._setupCachedList(layerId)

    def _setupCachedSurface(self, layerId):
        tileLayer = self.mapLayers[layerId].map
        cachedSurface = self._createCachedSurface(tileLayer)
        self._drawLayerToSurface(tileLayer, cachedSurface)
        self.cachedLayerRenderObject[layerId] = cachedSurface

    def _setupCachedList(self, layerId):
        tileLayer = self.mapLayers[layerId].map
        cacheList = []

        for rowIdx, row in enumerate(tileLayer):
            tileYPosition = rowIdx * self.tileSets[0].getTileHeight()
            for colIdx, tile in enumerate(row):
                tileXPosition = colIdx * self.tileSets[0].getTileWidth()
                if not tile == 0:
                    cacheList.append((tile, (tileXPosition, tileYPosition)))

        self.cachedLayerRenderObject[layerId] = cacheList

    def _drawLayerToSurface(self, tileLayer, surface, offset=None):
        if offset is None:
            offset = (0, 0)
        for rowIdx, row in enumerate(tileLayer):
            tileYPosition = rowIdx * self.tileSets[0].getTileHeight() + offset[1]
            for colIdx, tile in enumerate(row):
                tileXPosition = colIdx * self.tileSets[0].getTileWidth() + offset[0]
                if not tile == 0:
                    surface.blit(self._getTileBitmap(tile), (tileXPosition, tileYPosition), self._getTileRect(tile))


    def _loadMapLayer(self, layer, layerId=0):
        layerObject = self.mapLayers[layerId] = TileMap.MapLayer(layer)

        if not layerObject.getName() in self.mapLayerTypes:
            self.mapLayerTypes[layerObject.getName()] = []

        self.mapLayerTypes[layerObject.getName()].append(layerObject)

        if self.mapLayers[layerId].isVisible():
            self._setupCachedLayer(layerId)

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

    def getTileWidth(self):
        return self.tileSets[0].getTileWidth()

    def getTileHeight(self):
        return self.tileSets[0].getTileHeight()

    def getTilesAtPosition(self, x, y, mapType):
        result = []

        try:
            if mapType in self.mapLayerTypes:
                tileWidth = self.getTileWidth()
                tileHeight = self.getTileHeight()
                modifiedX = int(x/tileWidth)
                modifiedY = int(y/tileHeight)
                for layer in self.mapLayerTypes[mapType]:
                    tileValue = layer.map[modifiedY][modifiedX]
                    if not tileValue == 0:
                        result.append(TileMap.Tile(pygame.Rect(modifiedY, modifiedX, tileWidth, tileHeight), tileValue))
        except:
            print("Could not get tile information for TileMap at position: (%d,%d), type: %s, (%s)" % (x, y, mapType, sys.exc_info()[0]))

        return result

    def getTilesOnRect(self, rect, mapType=None):
        result = set()
        layerContainer = self.mapLayerTypes[mapType] if (not mapType is None and mapType in self.mapLayerTypes) else [layer for layerList in self.mapLayerTypes.values() for layer in layerList]
        tileWidth = self.getTileWidth()
        tileHeight = self.getTileHeight()
        for mapLayer in layerContainer:
            for x in range(rect.x/self.getTileWidth(), (rect.x+rect.w)/self.getTileWidth()+1):
                for y in range(rect.y/self.getTileHeight(), (rect.y+rect.h)/self.getTileHeight()+1):
                    tile = mapLayer.map[y][x];
                    if tile > 0:
                        result.add((x*tileWidth,y*tileHeight,tileWidth,tileHeight))
        return result

    def getTilesOfType(self, tileTypes, mapType=None):
        if not isinstance(tileTypes, list):
            tileTypes = [tileTypes]

        result = self.getTiles(mapType)
        result = filter(lambda x: x.value in tileTypes, result)

        return result

    def getTiles(self, mapType=None):
        result = []
        layerContainer = self.mapLayerTypes[mapType] if (not mapType is None and mapType in self.mapLayerTypes) else [layer for layerList in self.mapLayerTypes.values() for layer in layerList]
        for mapLayer in layerContainer:
            for x in range(mapLayer.getWidth()):
                for y in range(mapLayer.getHeight()):
                    if not mapLayer.map[x][y] == 0:
                        result.append(((y,x), mapLayer.map[x][y]))

        return result

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

        for layer, tileLayer in self.mapLayers.iteritems():
            if layer in self.cachedLayerRenderObject:
                cachedLayer = self.cachedLayerRenderObject[layer]
                if isinstance(cachedLayer, pygame.Surface):
                    renderRect = pygame.Rect(-objectPosition[0], -objectPosition[1], display.getScreenWidth(), display.getScreenHeight())
                    screen.blit(cachedLayer, (0, 0), renderRect)
                elif isinstance(cachedLayer, list):
                    for tile in cachedLayer:
                        tilePosition = [tile[1][0] + objectPosition[0], tile[1][1] + objectPosition[1]]
                        screen.blit(self._getTileBitmap(tile[0]), tilePosition, self._getTileRect(tile[0]))
            #else:
                #self._drawLayerToSurface(tileLayer, screen, offset)
