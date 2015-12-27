import pygame

class Timeout(object):
    def __init__(self, callback, milliseconds, repeats=1):
        self.repeats = repeats
        self._isRunning = True
        self.maxTime = milliseconds / 1000.0
        self.currentTime = self.maxTime
        self.callback = callback

    def tick(self, delta):
        if self._isRunning:
            self.currentTime -= delta
            if self.currentTime <= 0:
                self.callback()
                if self.repeats > 0:
                    self.repeats -= 1
                if self.repeats == 0:
                    self._isRunning = False
                else:
                    if abs(self.currentTime) < self.maxTime:
                        self.currentTime = self.maxTime + self.currentTime
                    else:
                        self.currentTime = self.maxTime

    @property
    def valid(self):
        return self._isRunning
