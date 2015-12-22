from ..awgl.modules import *
from ..awgl.objs import *

images.addToGlobalLoadList([
    ("tile-map-1", "tile-map-1.png")
])

class TMDefaultWorld(TileMap.TileMap):
    def __init__(self):
        super(TMDefaultWorld, self).__init__(images.getImage("tile-map-1"), 32, 32)
        self.scaleTiles(2, 2)
        self.setupDefaultTiles()
        self.loadMap("default.json")
        #self.loadMapLayer("default_default-world.csv", 0)
        #self.loadMapLayer("default_default-objects.csv", 1)
