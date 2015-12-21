import pygame

class Timeout():
    def __init__(self, callback, milliseconds, repeats=1):
        self.repeats = repeats
        self.isRunning = True
        self.maxTime = milliseconds / 1000.0
        self.currentTime = self.maxTime
        self.callback = callback

    def tick(self, delta):
        if self.isRunning:
            self.currentTime -= delta
            if self.currentTime <= 0:
                self.callback()
                if not self.repeats == 0:
                    if self.repeats > 0:
                        self.repeats -= 1
                    if not self.repeats == 0:
                        if abs(self.currentTime) < self.maxTime:
                            self.currentTime = self.maxTime + self.currentTime
                        else:
                            self.currentTime = self.maxTime
                    else:
                        self.isRunning = False

    def isValid(self):
        return self.isRunning
