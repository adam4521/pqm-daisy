"""Place a polygone line with the clicks of the mouse."""

import math
import pygame
import time
import random
from pygame.locals import *

RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (150, 150, 150)

pygame.init()
screen = pygame.display.set_mode((640, 240))

drawing = False
running = True
frames = 0
seconds = int(time.time())


while running:

    screen.fill(GRAY)
    points = []
    for t in range(0, 640):
        points.append((t, 100+int(50*math.sin(t*math.pi/180)) + 30*(random.random() - 0.5)))


    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    if len(points)>1:
        rect = pygame.draw.lines(screen, RED, False, points, 2)

    pygame.display.update()
    frames = frames + 1

    newtime = time.time() 
    if int(newtime) != seconds:
        seconds = int(newtime)
        print("FPS: " + str(frames))
        frames = 0

#    time.sleep(0.1)

pygame.quit()

