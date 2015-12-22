import pygame, math

COLOR_FRAMES = [
    [255,0,0],
    [255,255,0],
    [0,255,0],
    [0,255,255],
    [0,0,255],
    [255,0,255],
    [255,0,0]
]

def vectorLerp(a, b, pos):
    result = []

    for idx, ele in enumerate(a):
        result.append(ele * (1-pos) + b[idx] * (pos))

    return result

def getLineColor(pos):
    pos = pos % float(len(COLOR_FRAMES)-1)

    a = int(math.floor(pos))
    b = int(math.ceil(pos))


    colorElement = vectorLerp(COLOR_FRAMES[a], COLOR_FRAMES[b], pos-a)
    colorElement = map(lambda x: int(x), colorElement)
    return pygame.Color(*colorElement)

def renderGradientToScreen(surface, screenWidth, screenHeight):
    for i in range(screenWidth):
        color = gradient.getLineColor((i/float(screenWidth))*(len(COLOR_FRAMES)-1))
        startPos = (i, 0)
        endPos = (i, screenHeight)
        pygame.draw.line(surface, color, startPos, endPos)
