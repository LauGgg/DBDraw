import pygame as pg
from colors import Colors
from text import renderText
from SQLConstants import SQLConstants

class Relation(Colors, SQLConstants):
    space = 200
    entityWidth = 120

    def __init__(self, E1, E2, relation, pos, attributes = [], name=""):
        self.E1 = E1
        self.E2 = E2
        self.relation = relation
        self.attributes = attributes
        self.name = name
        self.pos = pos
        self.pos = (0, 0)

    def dist(self, pos):
        center = (self.pos[0] + self.entityWidth + self.space // 2, self.pos[1] + max(len(self.E1.attributes), len(self.E2.attributes)) * 22 + 35)
        return (center[0] - pos[0])**2 + (center[1] - pos[1])**2

    def renderArrow(self, scr, pos, left):
        if left:
            points = [(pos[0], pos[1]), (pos[0] + 10, pos[1] + 4), (pos[0] + 6, pos[1]), (pos[0] + 10, pos[1] - 4)]
        else:
            points = [(pos[0], pos[1]), (pos[0] - 10, pos[1] + 4), (pos[0] - 6, pos[1]), (pos[0] - 10, pos[1] - 4)]
        pg.draw.polygon(scr, (0,0,0), points)    
    
    def render(self, scr):
        self.E1.render(scr, (self.pos[0], self.pos[1]), self.entityWidth)
        self.E2.render(scr, (self.pos[0] + self.entityWidth + self.space, self.pos[1]), self.entityWidth)
        polySize = (90, 70)
        points = [
            (self.pos[0] + self.entityWidth + self.space // 2 - polySize[0] // 2, self.pos[1] + 15 + polySize[1] // 2), 
            (self.pos[0] + self.entityWidth + self.space // 2, self.pos[1] + 15), 
            (self.pos[0] + self.entityWidth + self.space // 2 + polySize[0] // 2, self.pos[1] + 15 + polySize[1] // 2), 
            (self.pos[0] + self.entityWidth + self.space // 2, self.pos[1] + 15 + polySize[1])
        ]
        pg.draw.polygon(scr, self.LIGHT_BLUE, points)
        pg.draw.polygon(scr, self.BLACK, points, 1)
        if self.name != "":
            renderText(scr, self.name, (self.pos[0] + self.entityWidth + self.space // 2, self.pos[1] + 4 + polySize[1] // 2), header=True, center=True)
        pg.draw.line(scr, self.BLACK, (self.pos[0] + self.entityWidth, self.pos[1] + 15 + polySize[1] // 2), points[0], 1)
        pg.draw.line(scr, self.BLACK, (self.pos[0] + self.entityWidth + self.space, self.pos[1] + 15 + polySize[1] // 2), points[2], 1)
        if self.relation[0] == self.ONE:
            self.renderArrow(scr, (self.pos[0] + self.entityWidth, self.pos[1] + 15 + polySize[1] // 2), True)
        elif self.relation[1] == self.ONE:
            self.renderArrow(scr, (self.pos[0] + self.entityWidth + self.space, self.pos[1] + 15 + polySize[1] // 2), False)
        if self.attributes != []:
            w = 60
            rect = (self.pos[0] + self.entityWidth + self.space // 2 - w // 2, self.pos[1] - (len(self.attributes) + 1) * 22 - 4, w, len(self.attributes) * 22 + 8)
            pg.draw.rect(scr, self.BLACK, rect, 1)
            for i, attribute in enumerate(self.attributes):
                attribute.render(scr, (self.pos[0] + self.entityWidth + self.space // 2, self.pos[1] - (len(self.attributes) + 1) * 22 + i * 22), center=True)
            h = (points[1][1] - (rect[1] + rect[3]))
            dots = 5
            d = h / dots
            for j in range(dots):
                if j % 2 == 0:
                    pg.draw.line(scr, self.BLACK, (points[1][0], points[1][1] - d - d * j), (points[1][0], points[1][1] - d * j), 1)
