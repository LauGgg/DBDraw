from colors import Colors
import pygame as pg

class Line(Colors):
    def __init__(self, points = []):
        self.points = points
        self.selected = True
    
    def render(self, scr):
        if self.selected:
            color = self.PURPLE
        else:
            color = self.BLACK
        if len(self.points) == 0:
            pass
        elif len(self.points) == 1:
            
            pg.draw.circle(scr, color, self.points[0], 4)
        else:
            for i in range(len(self.points) - 1):
                pg.draw.line(scr, color, self.points[i], self.points[i + 1], 2)