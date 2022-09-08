import thorpy
import math
import pygame
import time
import random
from pygame.locals import *

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (150, 150, 150)
SCREEN = (640,480)
SCOPE_BOX = (540,480)
CONTROLS_BOX = (100,480)
BUTTON_SIZE = (100,50) 

pygame.init()
pygame.display.set_caption('pqm-daisy')
screen = pygame.display.set_mode(SCREEN)

drawing = False
running = True
frames = 0
seconds = int(time.time())


button1 = thorpy.make_button("Summary")
button2 = thorpy.make_button("Scope")
button3 = thorpy.make_button("FFT")
button4 = thorpy.make_button("Options")
button5 = thorpy.make_button("Unused")
button6 = thorpy.make_button("Unused")

buttons = [button1, button2, button3, button4, button5, button6]
for button in buttons:
    button.set_size(BUTTON_SIZE)

box = thorpy.Box(elements=buttons)

menu = thorpy.Menu(box) #create a menu for auto events handling
for element in menu.get_population():
    element.surface = screen

box.set_size(CONTROLS_BOX)
box.set_topleft((SCREEN[0]-CONTROLS_BOX[0],0))
#menu.play() #launch the menu




while running:

    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == pygame.K_q):
            running = False
        menu.react(event)

    points1 = []
    points2 = []
    for t in range(0, SCOPE_BOX[0]):
        points1.append((t, 100+int(50*math.sin(t*math.pi/180)) + 30*(random.random() - 0.5)))
        points2.append((t, 300+int(50*math.sin(t*math.pi/180)) + 30*(random.random() - 0.5)))


    pygame.draw.lines(screen, RED, False, points1, 2)
    pygame.draw.lines(screen, BLUE, False, points2, 2)
    box.blit()
    # button1.update()
    
    pygame.display.update()
    frames = frames + 1

    newtime = int(time.time())
    if newtime != seconds:
        seconds = newtime
        print("FPS: " + str(frames))
        frames = 0


pygame.quit()

