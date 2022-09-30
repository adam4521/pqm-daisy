import math
import random



FRAME_LENGTH = 540
FREQ = 60.0
T_DIV = 0.005



def make_capture():
    frame = []
    for s in range(0, FRAME_LENGTH):
        t = T_DIV*10.0*s/FRAME_LENGTH
        v1 = 50.0*math.sin(2.0*math.pi*FREQ*t) + 20.0*(random.random() - 0.5)
        i1 = 50.0*math.sin(2.0*math.pi*FREQ*t) + 20.0*(random.random() - 0.5)
        p1 = v1*i1
        frame.append((s, v1, i1, p1))
    return frame


def main():
    while 1:
        frame = make_capture()
        for e in frame:
            print('{:5d} {:12.4f} {:12.4f} {:12.4f}'.format(*e))


main()




