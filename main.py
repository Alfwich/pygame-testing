import pygame, sys, os, math, random
import colors, time, images, fonts, sounds, events, gradient
import StaticObject, RenderList, Camera, AnimatedObject
import SOFrog, SOStaticText, AOWalkingGuy
from pygame.locals import *

FPS = 60
SCREEN_SIZE = (1000, 1000)
TITLE = "Test Game"

images.addToGlobalLoadList([
])

sounds.addToGlobalLoadList([
    ("startup", "windows-logon.wav")
])

# Inits pygame and various components
def init():
    pygame.init()
    images.init()
    fonts.init()
    colors.init()
    events.init()
    pygame.display.set_caption(TITLE)

    # Init images from their respective lists. This allows game classes
    # to define images and sounds that will be used at declaration time
    images.loadGlobalImageList()
    sounds.loadGlobalSoundList()

def main():
    init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    if screen is None or clock is None:
        print("Could not create screen or clock object.", screen, clock)
        return

    mainRenderList = RenderList.RenderList()
    mainCamera = Camera.Camera()
    mainCamera.locked = False

    coolText = SOStaticText.SOStaticText("Fuck you man!")
    mainRenderList.addObject(coolText)

    animatedGuy = AOWalkingGuy.AOWalkingGuy()
    mainRenderList.addObject(animatedGuy)

    def quitApplication(event):
        pygame.quit()
        sys.exit()

    mainCameraVelocity = [0, 0]
    def updateCameraVelocityX(x):
        if abs(x) > 0.2:
            mainCameraVelocity[0] = x
        else:
            mainCameraVelocity[0] = 0

    def updateCameraVelocityY(y):
        if abs(y) > 0.2:
            mainCameraVelocity[1] = y
        else:
            mainCameraVelocity[1] = 0

    if pygame.joystick.get_count() > 0:
        js = pygame.joystick.Joystick(0)
        js.init()

    pygame.joystick.init()

    events.bindQuitEvent(quitApplication)
    events.bindKeyDownEvent(["q"], quitApplication)
    #events.bindMouseMotionEvent(lambda e: mainCamera.moveOffset(e.rel[0], e.rel[1]))

    events.bindJoystickAxisMotionEvent(0, 3, lambda e, v: updateCameraVelocityY(v))
    events.bindJoystickAxisMotionEvent(0, 4, lambda e, v: updateCameraVelocityX(v))
    #events.bindMouseDownEvent([1], lambda e: mainCamera.unlock())
    #events.bindMouseUpEvent([1], lambda e: mainCamera.lock())
    events.bindKeyDownEvent(["g"], lambda e: sounds.playSoundOnce("startup"))
    while True:
        # Limit framerate to the desired FPS
        delta = clock.tick(FPS)/1000.0

        # Handle game events through the event queue
        events.handleEvents()

        # Call the tick methos from any tickable object
        events.tickObjects(delta)
        mainCamera.moveOffset( mainCameraVelocity[0] * delta * 100, mainCameraVelocity[1] * delta * 100)

        # Draw screen
        screen.fill(colors.getColor(colors.BLACK))
        mainRenderList.render(screen, mainCamera)
        pygame.display.update()

if __name__ == "__main__":
    main()
