import thorpy
import math
import pygame
import time
import random
from pygame.locals import *

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
GRAY = (150, 150, 150)
SCREEN = (640,480)
SCOPE_BOX = (540,480)
CONTROLS_BOX = (100,480)
BUTTON_SIZE = (100,50) 
TEXT_SIZE = (100,12)

pygame.init()
pygame.display.set_caption('pqm-daisy')
screen = pygame.display.set_mode(SCREEN)

strings = ['Running', 'This.', 'is', 'some', 'test text', '12345678']

# update text message strings, called periodically
def set_text_strings(texts, strings):
    i=0
    for s in strings:
        texts[i].set_text(s)
        i=i+1



# for button in buttons:
buttons = []
for s in ['Run/Stop', 'Mode', 'Logging', 'Scales', 'Options', 'About']:
    button = thorpy.make_button(s)
    button.set_size(BUTTON_SIZE)
    buttons.append(button)


texts = []
for s in range(0,7):
    text = thorpy.make_text('1234567890')
    text.set_size(TEXT_SIZE)
    texts.append(text)

capturing = True
def start_stop_reaction(event):
   global capturing
   if capturing == True:
       capturing = False
       strings[0] = 'Stopped'
   else:
       capturing = True
       strings[0] = 'Running'

 
uibox = thorpy.Box(elements=[*buttons, *texts])

# setup some reactions
first_reaction = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT, reac_func=start_stop_reaction, event_args={"el": buttons[0], "id": thorpy.constants.EVENT_UNPRESS})
uibox.add_reaction(first_reaction)



menu = thorpy.Menu(uibox) #create a menu for auto events handling
for element in menu.get_population():
    element.surface = screen

uibox.set_size(CONTROLS_BOX)
uibox.set_topleft((SCREEN[0]-CONTROLS_BOX[0],0))
#menu.play() #launch the menu


def get_capture(points1, points2, points3):
    for t in range(0, SCOPE_BOX[0]):
        points1.append((t, 50*math.sin(t*math.pi/180) + 20*(random.random() - 0.5)))
        points2.append((t, 50*math.sin(t*math.pi/180) + 20*(random.random() - 0.5)))
        points3.append((t, points1[t][1]*points2[t][1]))
    return points1, points2, points3


def to_screen_coordinates(points1, points2, points3):
    plot1 = []
    plot2 = []
    plot3 = []
    for t in range(0, len(points1)):
        # invert y axis in plot coordinates, which increase from top of the display downwards
        plot1.append((t, 100-int(points1[t][1])))
        plot2.append((t, 400-int(points2[t][1])))
        plot3.append((t, 250-int(0.05*points3[t][1])))
    return plot1, plot2, plot3


running = True
frames = 0
seconds = int(time.time())

while running:

    # deal with the event queue
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == pygame.K_q):
            running = False
        menu.react(event)

    # update line data
    if capturing:
        plot1, plot2, plot3 = to_screen_coordinates(*get_capture([],[],[]))

    # regenerate display 
    screen.fill(GRAY)
    pygame.draw.lines(screen, RED, False, plot1, 2)
    pygame.draw.lines(screen, BLUE, False, plot2, 2)
    pygame.draw.lines(screen, MAGENTA, False, plot3, 2)
    uibox.blit()
    # uibox.update()
    
    frames = frames + 1
    newtime = int(time.time())

    # refresh the information box every second
    if newtime != seconds:
        seconds = newtime
        strings[1] = "FPS: " + str(frames)
        set_text_strings(texts, strings)
        frames = 0


    pygame.display.update()

pygame.quit()

