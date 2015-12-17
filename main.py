import pygame, sys, os
from pygame.locals import *

def main():
    pygame.init()
    surface = pygame.display.set_mode((400,300))
    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                    pygame.quit()
                    return
            pygame.display.update()

if __name__ == "__main__":
    main()
