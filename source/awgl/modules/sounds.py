import pygame

SOUND_LOAD_TEMPLATE = "data/sound/%s"
_loadedSounds = {}
_globalSoundLoadList = []

def init():
    pygame.mixer.init()
    sounds.loadGlobalSoundList()

def addToGlobalLoadList(newList):
    for asset in newList:
        _globalSoundLoadList.append(asset)

def loadGlobalSoundList():
    loadSoundList(_globalSoundLoadList)

def loadSound(name, path):
    sound = pygame.mixer.Sound(SOUND_LOAD_TEMPLATE % path)
    _loadedSounds[name] = sound

def loadSoundList(soundList):
    for asset in soundList:
        loadSound(*asset)

def getSound(name):
    if name in _loadedSounds:
        return _loadedSounds[name]
    else:
        print("Could not load sound for name: '%s'" % name)
        return None

def playSoundOnce(name):
    if name in _loadedSounds:
        return _loadedSounds[name].play()
    else:
        print("Could not find sound for name: '%s'" % name)

def stopAllSounds():
    for key, sound in _loadedSounds.iteritems():
        sound.stop()
