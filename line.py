from colors import Colors
import pygame as pg
from SQLConstants import SQLConstants
from arrow import renderArrow
# from math import sqrt

class Line(Colors, SQLConstants):
    def __init__(self, points = []):
        self.points = points
        self.selected = True
        self.arrow = False
    
    def click(self):
        self.selected = True

    def finish(self):
        self.selected = False

    def deletePoint(self):
        self.points.pop()
        if self.arrow:
            self.arrow = False

    def addPoint(self, pos, entities):
        for entity in entities:
            if entity.type == self.ENTITYSET:
                if self.connect(pos, entity):
                    return True
        if len(self.points) == 0:
            self.points.append(pos)
            return
        if abs(pos[0] - self.points[-1][0]) < 12:
            self.points.append((self.points[-1][0], pos[1]))
        elif abs(pos[1] - self.points[-1][1]) < 12:
            self.points.append((pos[0], self.points[-1][1]))
        return False

    def collide(self, pos):
        for i in range(len(self.points) - 1):
            if self.points[i][0] == self.points[i + 1][0]:
                if (self.points[i][1] <= pos[1] <= self.points[i + 1][1]) or (self.points[i][1] >= pos[1] >= self.points[i + 1][1]):
                    if abs(self.points[i][0] - pos[0]) < 10:
                        return True
            else:
                if (self.points[i][0] <= pos[0] <= self.points[i + 1][0]) or (self.points[i][0] >= pos[0] >= self.points[i + 1][0]):
                    if abs(self.points[i][1] - pos[1]) < 10:
                        return True
        return False
                
    def connect(self, pos, entitySet):
        for i in range(len(entitySet.attributes)):
            anchorR =  (entitySet.pos[0] + entitySet.width, 42 + entitySet.pos[1] + i * 22)
            anchorL =  (entitySet.pos[0], 42 + entitySet.pos[1] + i * 22)
            if self.sqDist(pos, anchorR) < 40:
                self.propagate(anchorR)
                if len(self.points) != 0:
                    self.finish()
                    self.arrow = True
                self.points.append(anchorR)
                return True
            elif self.sqDist(pos, anchorL) < 40:
                self.propagate(anchorL)
                if len(self.points) != 0:
                    self.finish()
                    self.arrow = True
                self.points.append(anchorL)
                return True
    
    def propagate(self, lockedPoint):
        if len(self.points) < 2:
            return
        if abs(self.points[-1][0] - lockedPoint[0]) < 12:
            self.points[-1] = (lockedPoint[0], self.points[-1][1])
        elif abs(self.points[-1][1] - lockedPoint[1]) < 12:
            self.points[-1] = (self.points[-1][0], lockedPoint[1])

    def sqDist(self, posA, posB):
        return abs(posA[0] - posB[0])**2 + abs(posA[1] - posB[1])**2

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
            if self.arrow:
                if self.points[-1][0] < self.points[-2][0]:
                    renderArrow(scr, self.points[-1], left=True)
                else:
                    renderArrow(scr, self.points[-1], right=True)
