import pygame
import RenderList

class SortedRenderList(RenderList.RenderList):

    def __init__(self, name, cmpFunction=lambda x: x.getPositionY()):
        super(SortedRenderList, self).__init__(name)
        self.compareFunction = cmpFunction
        self._isSorted = False
        self._continouslySort = True

    def _sortObjects(self):
        self.objects.sort(key=self.compareFunction)
        self._isSorted = True

    def setContinuousSort(self, newSortOption):
        self._continouslySort = newSortOption

    def addObject(self, obj):
        super(SortedRenderList, self).addObject(obj)
        self._isSorted = False

    def removeObject(self, removeObj):
        super(SortedRenderList, self).removeObject(obj)
        self._isSorted = False

    def render(self, screen, camera=None):
        if self._continouslySort or not self._isSorted:
            self._sortObjects()
        super(SortedRenderList, self).render(screen, camera)
