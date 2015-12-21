import fonts, pygame, StaticObject as SO

class SOStaticText(SO.StaticObject):
    def __init__(self, text):
        super(SOStaticText, self).__init__()
        self.setBitmap(fonts.renderTextSurface(text))

    def updateText(self, newText):
        self.setBitmap(fonts.renderTextSurface(newText))
