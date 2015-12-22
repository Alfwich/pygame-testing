import pygame
from ..objs import Animation

_cachedAnimations  = {}

def addAnimation(name, frames):
    if not isinstance(frames, list):
        frames = [frames]
    newAnimation = Animation.Animation()
    rectFrames = map(lambda x: pygame.Rect(*x), frames)

    for frame in rectFrames:
        newAnimation.addFrame(frame)

    _cachedAnimations[name] = newAnimation

def addFramesToAnimation(name, frames):
    if not isinstance(frames, list):
        frames = [frames]

    rectFrames = map(lambda x: pygame.Rect(*x), frames)

    if name in _cachedAnimations:
        for frame in rectFrames:
            _cachedAnimations[name].addFrame(frame)

def getAnimation(name):
    return _cachedAnimations[name] if name in _cachedAnimations else None
