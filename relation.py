import pygame as pg
from colors import Colors
from text import renderText
from SQLConstants import SQLConstants
from DBRender import DBRender
from arrow import renderArrow

class Relation(DBRender, Colors, SQLConstants):
    space = 250
    polySize = (170, 90)

    def __init__(self, E1, E2, relation, participation, attributes = [], name=""):
        super().__init__(E1.pos, self.RELATION, name, attributes)
        self.E1 = E1
        self.E2 = E2
        E1.setInRelation()
        E2.setInRelation()
        self.relation = relation
        self.participation = participation
        self.align = self.HORIZONTAL if abs(self.E1.pos[0] - self.E2.pos[0]) > abs(self.E1.pos[1] - self.E2.pos[1]) else self.VERTICAL

    def move(self, dx, dy):
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)
        
    def cancelRelation(self):
        self.E1.removeRelation()
        self.E2.removeRelation()

    def collide(self, pos):
        if self.align == self.HORIZONTAL:
            return pg.Rect(self.pos[0] + self.E1.width + self.space // 2 - self.polySize[0] // 2, self.pos[1] + 15, self.polySize[0], self.polySize[1]).collidepoint(pos)
        else:
            return pg.Rect(self.pos[0] + self.E1.width // 2 - self.polySize[0] // 2, self.pos[1] + self.E1.getHeight() + self.space // 2 - self.polySize[1] // 2, self.polySize[0], self.polySize[1]).collidepoint(pos)

    def cycleAlign(self):
        self.align = self.HORIZONTAL if self.align == self.VERTICAL else self.VERTICAL

    def cycleRelation(self, left=False, right=False):
        if left:
            if self.relation[0] == self.ONE:
                self.relation[0] = self.MANY
            else:
                self.relation[0] = self.ONE
        elif right:
            if self.relation[1] == self.ONE:
                self.relation[1] = self.MANY
            else:
                self.relation[1] = self.ONE
            
    def cycleParticipation(self, left=False, right=False):
        if left:
            if self.participation[0] == self.TOTAL:
                self.participation[0] = self.PARTIAL
            else:
                self.participation[0] = self.TOTAL
        elif right:
            if self.participation[1] == self.TOTAL:
                self.participation[1] = self.PARTIAL
            else:
                self.participation[1] = self.TOTAL

    def render(self, scr, state):
        if self.align == self.HORIZONTAL:
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
                if self.weak:
                    points2 = [(points[0][0] - 5, points[0][1]), (points[1][0], points[1][1] - 5), (points[2][0] + 5, points[2][1]), (points[3][0], points[3][1] + 5)]
                    pg.draw.polygon(scr, self.PURPLE, points2, 1)
            else:
                pg.draw.polygon(scr, self.BLACK, points, 1)
                if self.weak:
                    points2 = [(points[0][0] - 5, points[0][1]), (points[1][0], points[1][1] - 3), (points[2][0] + 5, points[2][1]), (points[3][0], points[3][1] + 3)]
                    pg.draw.polygon(scr, self.BLACK, points2, 1)
            lineOffset = 5 if self.weak else 0
            if self.name != "":
                renderText(scr, self.name, (self.pos[0] + self.E1.width + self.space // 2, self.pos[1] + 4 + self.polySize[1] // 2), header=True, center=True, font_size=18)
            if self.participation[0] == self.TOTAL:
                pg.draw.line(scr, self.BLACK, (self.pos[0] + self.E1.width, self.pos[1] + 12 + self.polySize[1] // 2), (points[0][0] - lineOffset, points[0][1] - 3), 1)
                pg.draw.line(scr, self.BLACK, (self.pos[0] + self.E1.width, self.pos[1] + 18 + self.polySize[1] // 2), (points[0][0] - lineOffset, points[0][1] + 3), 1)
            else:
                pg.draw.line(scr, self.BLACK, (self.pos[0] + self.E1.width, self.pos[1] + 15 + self.polySize[1] // 2), (points[0][0] - lineOffset, points[0][1]), 1)
            if self.participation[1] == self.TOTAL:
                pg.draw.line(scr, self.BLACK, (self.pos[0] + self.E1.width + self.space, self.pos[1] + 12 + self.polySize[1] // 2), (points[2][0] + lineOffset, points[2][1] - 3), 1)
                pg.draw.line(scr, self.BLACK, (self.pos[0] + self.E1.width + self.space, self.pos[1] + 18 + self.polySize[1] // 2), (points[2][0] + lineOffset, points[2][1] + 3), 1)
            else:
                pg.draw.line(scr, self.BLACK, (self.pos[0] + self.E1.width + self.space, self.pos[1] + 15 + self.polySize[1] // 2), (points[2][0] + lineOffset, points[2][1]), 1)
            if self.relation[0] == self.ONE:
                if self.participation[0] == self.TOTAL:
                    renderArrow(scr, (self.pos[0] + self.E1.width, self.pos[1] + 12 + self.polySize[1] // 2), left=True)
                    renderArrow(scr, (self.pos[0] + self.E1.width, self.pos[1] + 18 + self.polySize[1] // 2), left=True)
                else:
                    renderArrow(scr, (self.pos[0] + self.E1.width, self.pos[1] + 15 + self.polySize[1] // 2), left=True)
            if self.relation[1] == self.ONE:
                if self.participation[1] == self.TOTAL:
                    renderArrow(scr, (self.pos[0] + self.E1.width + self.space, self.pos[1] + 12 + self.polySize[1] // 2), right=True)
                    renderArrow(scr, (self.pos[0] + self.E1.width + self.space, self.pos[1] + 18 + self.polySize[1] // 2), right=True)
                else:
                    renderArrow(scr, (self.pos[0] + self.E1.width + self.space, self.pos[1] + 15 + self.polySize[1] // 2), right=True)
            if len(self.attributes) != 0:
                w = 140
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
        else:
            E1h = self.E1.getHeight()
            self.E1.pos = (self.pos[0], self.pos[1])
            self.E2.pos = (self.pos[0], self.pos[1] + self.space + E1h)
            points = [
                (self.pos[0] + self.E1.width // 2 - self.polySize[0] // 2, self.pos[1] + E1h + self.space // 2), 
                (self.pos[0] + self.E1.width // 2, self.pos[1] + E1h - self.polySize[1] // 2 + self.space // 2), 
                (self.pos[0] + self.E1.width // 2  + self.polySize[0] // 2, self.pos[1] + E1h + self.space // 2), 
                (self.pos[0] + self.E1.width // 2, self.pos[1] + E1h + self.polySize[1] // 2 + self.space // 2)
            ]
            pg.draw.polygon(scr, self.LIGHT_BLUE, points)
            if self.selected:
                pg.draw.polygon(scr, self.PURPLE, points, 1)
                if self.weak:
                    points2 = [(points[0][0] - 5, points[0][1]), (points[1][0], points[1][1] - 5), (points[2][0] + 5, points[2][1]), (points[3][0], points[3][1] + 5)]
                    pg.draw.polygon(scr, self.PURPLE, points2, 1)
            else:
                pg.draw.polygon(scr, self.BLACK, points, 1)
                if self.weak:
                    points2 = [(points[0][0] - 5, points[0][1]), (points[1][0], points[1][1] - 3), (points[2][0] + 5, points[2][1]), (points[3][0], points[3][1] + 3)]
                    pg.draw.polygon(scr, self.BLACK, points2, 1)
            lineOffset = 5 if self.weak else 0
            if self.name != "":
                renderText(scr, self.name, (self.pos[0] + self.E1.width // 2, self.pos[1] + E1h + self.space // 2 - 12), header=True, center=True)
            if self.participation[0] == self.TOTAL:
                pg.draw.line(scr, self.BLACK, (self.pos[0] + self.E1.width // 2 - 3, self.pos[1] + E1h), (points[1][0] - 3, points[1][1] - lineOffset), 1)
                pg.draw.line(scr, self.BLACK, (self.pos[0] + self.E1.width // 2 + 3, self.pos[1] + E1h), (points[1][0] + 3, points[1][1] - lineOffset), 1)
            else:
                pg.draw.line(scr, self.BLACK, (self.pos[0] + self.E1.width // 2, self.pos[1] + E1h), (points[1][0], points[1][1] - lineOffset), 1)
            if self.participation[1] == self.TOTAL:
                pg.draw.line(scr, self.BLACK, (self.pos[0] + self.E1.width // 2 - 3, self.pos[1] + E1h + self.space), (points[3][0] - 3, points[3][1] + lineOffset), 1)
                pg.draw.line(scr, self.BLACK, (self.pos[0] + self.E1.width // 2 + 3, self.pos[1] + E1h + self.space), (points[3][0] + 3, points[3][1] + lineOffset), 1)
            else:
                pg.draw.line(scr, self.BLACK, (self.pos[0] + self.E1.width // 2, self.pos[1] + E1h + self.space), (points[3][0], points[3][1] + lineOffset), 1)
            if self.relation[0] == self.ONE:
                if self.participation[0] == self.TOTAL:
                    renderArrow(scr, (self.pos[0] + self.E1.width // 2 - 3, self.pos[1] + E1h), up=True)
                    renderArrow(scr, (self.pos[0] + self.E1.width // 2 + 3, self.pos[1] + E1h), up=True)
                else:
                    renderArrow(scr, (self.pos[0] + self.E1.width // 2, self.pos[1] + E1h), up=True)
            if self.relation[1] == self.ONE:
                if self.participation[1] == self.TOTAL:
                    renderArrow(scr, (self.pos[0] + self.E1.width // 2 - 3, self.pos[1] + self.space + E1h), down=True)
                    renderArrow(scr, (self.pos[0] + self.E1.width // 2 + 3, self.pos[1] + self.space + E1h), down=True)
                else:
                    renderArrow(scr, (self.pos[0] + self.E1.width // 2, self.pos[1] + self.space + E1h), down=True)
