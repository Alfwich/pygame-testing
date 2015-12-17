import pygame, sys, os, colors, time, random, images, fonts
from pygame.locals import *

FPS = 60
SCREEN_SIZE = (1000, 1000)
TITLE = "Test Game"
IMAGE_LOAD_TEMPLATE = "src\img\%s"
IMAGE_LOAD_LIST = [
    ("frog", "frog-face.png")
]

# Inits pygame and various components
def init():
    pygame.init()
    fonts.init()
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    # Init images from list
    for asset in IMAGE_LOAD_LIST:
        images.loadImage(asset[0], IMAGE_LOAD_TEMPLATE % asset[1])

    return screen, clock

def getRandomCoord():
    return (random.randint(0, SCREEN_SIZE[0]), random.randint(0, SCREEN_SIZE[1]))

def main():
    screen, clock = init()
    if screen is None or clock is None:
        print("Could not create screen or clock object.", screen, clock)
        return

    coolText = fonts.renderTextSurface("Cool Text; Brah!")
    while True:
        # Limit framerate to 60fps
        clock.tick(FPS)

        # Handle game events
        for e in pygame.event.get():
            if e.type == QUIT:
                    pygame.quit()
                    return

        # Update positions of objects

        # Draw screen
        #screen.fill(colors.BLACK)
        for i in range(10):
            pygame.draw.line(screen, colors.randomColor(), getRandomCoord(), getRandomCoord(), 1)
        screen.blit(images.getImage("frog"), (10,10))
        screen.blit(coolText, (100,100))
        pygame.display.update()

if __name__ == "__main__":
    main()
