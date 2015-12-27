
class Animation():
    def __init__(self):
        self.frames = []

    def addFrame(self, rect):
        self.frames.append(rect)

    def __getitem__(self, frame):
        return self.frames[frame]
        
    def getFrameRect(self, frame):
        return self.frames[frame]

    def numberOfFrames(self):
        return len(self.frames)
