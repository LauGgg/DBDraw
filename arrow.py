import pygame as pg
from colors import Colors

def renderArrow(scr, pos, right=False, left=False, up=False, down=False):
        if right:
            points = [(pos[0], pos[1]), (pos[0] - 8, pos[1] + 3), (pos[0] - 6, pos[1]), (pos[0] - 8, pos[1] - 3)]
        elif left:
            points = [(pos[0], pos[1]), (pos[0] + 8, pos[1] + 3), (pos[0] + 6, pos[1]), (pos[0] + 8, pos[1] - 3)]
        elif up:
            points = [(pos[0], pos[1]), (pos[0] + 3, pos[1] + 8), (pos[0], pos[1] + 6), (pos[0] - 3, pos[1] + 8)]
        elif down:
            points = [(pos[0], pos[1]), (pos[0] + 3, pos[1] - 8), (pos[0], pos[1] - 6), (pos[0] - 3, pos[1] - 8)]
        pg.draw.polygon(scr, Colors.BLACK, points)

        # elif up:
        #     pass
