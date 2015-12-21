import pygame, random

BLACK = pygame.Color("#000000")
WHITE = pygame.Color("#ffffff")
RED = pygame.Color("#ff0000")
GREEN = pygame.Color("#00ff00")
BLUE = pygame.Color("#0000ff")
PURPLE = pygame.Color("#9b30ff")

def randomColor():
    return pygame.Color(random.randint(0,255), random.randint(0,255), random.randint(0,255))
