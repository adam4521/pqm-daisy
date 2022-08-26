"""Place a polygone line with the clicks of the mouse."""

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


while running:

    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == pygame.K_q):
            running = False
    
    points1 = []
    points2 = []
    for t in range(0, 639):
        points1.append((t, 100+int(50*math.sin(t*math.pi/180)) + 30*(random.random() - 0.5)))
        points2.append((t, 300+int(50*math.sin(t*math.pi/180)) + 30*(random.random() - 0.5)))


    pygame.draw.lines(screen, RED, False, points1, 2)
    pygame.draw.lines(screen, BLUE, False, points2, 2)

    pygame.display.update()
    frames = frames + 1

    newtime = time.time() 
    if int(newtime) != seconds:
        seconds = int(newtime)
        print("FPS: " + str(frames))
        frames = 0

#    time.sleep(0.1)

pygame.quit()

