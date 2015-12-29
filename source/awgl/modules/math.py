import math as pyMath

def vectorLerp(a, b, pos):
    result = []

    for idx, ele in enumerate(a):
        result.append(ele * (1-pos) + b[idx] * (pos))

    return result

def clamp(minValue, maxValue, value):
    return sorted([minValue, value, maxValue])[1]
