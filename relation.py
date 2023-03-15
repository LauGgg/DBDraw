import pygame as pg
from colors import Colors
from text import renderText
from SQLConstants import SQLConstants
from DBRender import DBRender

class Relation(DBRender, Colors, SQLConstants):
    space = 200
    polySize = (90, 70)

    def __init__(self, E1, E2, relation, attributes = [], name=""):
        super().__init__(E1.pos, self.RELATION, name, attributes)
        self.E1 = E1
        self.E2 = E2
        self.relation = relation
        
    
    def move(self, dx, dy):
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)
        pass

    def collide(self, pos):
        return pg.Rect(self.pos[0] + self.E1.width + self.space // 2 - self.polySize[0] // 2, self.pos[1] + 15, self.polySize[0], self.polySize[1]).collidepoint(pos)


    def renderArrow(self, scr, pos, left):
        if left:
            points = [(pos[0], pos[1]), (pos[0] + 10, pos[1] + 4), (pos[0] + 6, pos[1]), (pos[0] + 10, pos[1] - 4)]
        else:
            points = [(pos[0], pos[1]), (pos[0] - 10, pos[1] + 4), (pos[0] - 6, pos[1]), (pos[0] - 10, pos[1] - 4)]
        pg.draw.polygon(scr, (0,0,0), points)    

    def render(self, scr):
        self.E1.pos = (self.pos[0], self.pos[1])
        self.E2.pos = (self.pos[0] + self.E1.width + self.space, self.pos[1])
        points = [
            (self.pos[0] + self.E1.width + self.space // 2 - self.polySize[0] // 2, self.pos[1] + 15 + self.polySize[1] // 2), 
            (self.pos[0] + self.E1.width + self.space // 2, self.pos[1] + 15), 
            (self.pos[0] + self.E1.width + self.space // 2 + self.polySize[0] // 2, self.pos[1] + 15 + self.polySize[1] // 2), 
            (self.pos[0] + self.E1.width + self.space // 2, self.pos[1] + 15 + self.polySize[1])
        ]
        pg.draw.polygon(scr, self.LIGHT_BLUE, points)
        if self.selected:
            pg.draw.polygon(scr, self.PURPLE, points, 1)
        else:
            pg.draw.polygon(scr, self.BLACK, points, 1)
        if self.name != "":
            renderText(scr, self.name, (self.pos[0] + self.E1.width + self.space // 2, self.pos[1] + 4 + self.polySize[1] // 2), header=True, center=True)
        pg.draw.line(scr, self.BLACK, (self.pos[0] + self.E1.width, self.pos[1] + 15 + self.polySize[1] // 2), points[0], 1)
        pg.draw.line(scr, self.BLACK, (self.pos[0] + self.E1.width + self.space, self.pos[1] + 15 + self.polySize[1] // 2), points[2], 1)
        if self.relation[0] == self.ONE:
            self.renderArrow(scr, (self.pos[0] + self.E1.width, self.pos[1] + 15 + self.polySize[1] // 2), True)
        if self.relation[1] == self.ONE:
            self.renderArrow(scr, (self.pos[0] + self.E1.width + self.space, self.pos[1] + 15 + self.polySize[1] // 2), False)
        if len(self.attributes) != 0:
            w = 70
            rect = (self.pos[0] + self.E1.width + self.space // 2 - w // 2, self.pos[1] - (len(self.attributes) + 1) * 22 - 4, w, len(self.attributes) * 22 + 8)
            pg.draw.rect(scr, self.BLACK, rect, 1)
            for i, attribute in enumerate(self.attributes):
                attribute.render(scr, (self.pos[0] + self.E1.width + self.space // 2, self.pos[1] + (i - (len(self.attributes) + 1)) * 22), center=True)
            h = (points[1][1] - (rect[1] + rect[3]))
            dots = 5
            d = h / dots
            for j in range(dots):
                if j % 2 == 0:
                    pg.draw.line(scr, self.BLACK, (points[1][0], points[1][1] - d - d * j), (points[1][0], points[1][1] - d * j), 1)
