"""Place a polygone line with the clicks of the mouse."""

#ThorPy hello world tutorial : full code
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

pygame.init()
screen = pygame.display.set_mode(SCREEN)

drawing = False
running = True
frames = 0
seconds = int(time.time())


my_button = thorpy.make_button("Hello, world!") #just a useless button

menu = thorpy.Menu(my_button) #create a menu for auto events handling
for element in menu.get_population():
    element.surface = screen


my_button.center() #center the element on the screen
#my_button.set_topleft((100,100))
#menu.play() #launch the menu




while running:

    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == pygame.K_q):
            running = False
        menu.react(event)

    points1 = []
    points2 = []
    for t in range(0, 639):
        points1.append((t, 100+int(50*math.sin(t*math.pi/180)) + 30*(random.random() - 0.5)))
        points2.append((t, 300+int(50*math.sin(t*math.pi/180)) + 30*(random.random() - 0.5)))


    pygame.draw.lines(screen, RED, False, points1, 2)
    pygame.draw.lines(screen, BLUE, False, points2, 2)
    my_button.blit()
    # my_button.update()
    
    pygame.display.update()
    frames = frames + 1

    newtime = int(time.time())
    if newtime != seconds:
        seconds = newtime
        print("FPS: " + str(frames))
        frames = 0


pygame.quit()

