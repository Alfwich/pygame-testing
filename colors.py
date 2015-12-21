import pygame, random

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)

def randomColor():
    return pygame.Color(random.randint(0,255), random.randint(0,255), random.randint(0,255))
