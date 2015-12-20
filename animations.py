import pygame, Animation

_cachedAnimations  = {}

def addAnimation(name, frames):
    newAnimation = Animation.Animation()

    rectFrames = map(lambda x: pygame.Rect(*x), frames)
    for frame in rectFrames:
        newAnimation.addFrame(frame)

    _cachedAnimations[name] = newAnimation


def getAnimation(name):
    return _cachedAnimations[name] if name in _cachedAnimations else None
