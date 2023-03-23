import pygame as pg
from text import renderText
from colors import Colors
from DBRender import DBRender
from SQLConstants import SQLConstants

class EntitySet(DBRender, Colors, SQLConstants):
    def __init__(self, pos, width, name="", attributes=[]):
        super().__init__(pos, self.ENTITYSET, name, attributes)
        self.width = width
        self.rect = pg.Rect(self.pos[0], self.pos[1], width, 29)
        self.inRelation = False
    
    def collide(self, pos):
        return self.rect.collidepoint(pos)

    def setInRelation(self):
        self.inRelation = True
    
    def removeRelation(self):
        self.inRelation = False
    
    def move(self, dx, dy):
        if not self.inRelation:
            self.pos = (self.pos[0] + dx, self.pos[1] + dy)
            self.rect = pg.Rect(self.pos[0], self.pos[1], self.width, 35 + (len(self.attributes) * 22))
        
    def getHeight(self):
        return 35 + (len(self.attributes) * 22)
        
    def render(self, scr, state):
        self.rect = pg.Rect(self.pos[0], self.pos[1], self.width, 35 + (len(self.attributes) * 22))
        pg.draw.rect(scr, self.BLUE, (self.pos[0], self.pos[1], self.width, 29))
        if self.selected:
            pg.draw.rect(scr, self.PURPLE, (self.pos[0], self.pos[1], self.width, 29), 2)
            pg.draw.rect(scr, self.PURPLE, self.rect, 2)
        else:
            pg.draw.rect(scr, self.BLACK, (self.pos[0], self.pos[1], self.width, 29), 1)
            pg.draw.rect(scr, self.BLACK, self.rect, 1)
        renderText(scr, self.name, (self.pos[0] + 5, self.pos[1] + 5), header=True)
        for i, attribute in enumerate(self.attributes):
            attribute.render(scr, (self.pos[0] + 5, 32 + self.pos[1] + i * 22), weak=self.weak)
            if state == self.LINE:
                pg.draw.circle(scr, self.PURPLE, (self.pos[0] + self.width, 42 + self.pos[1] + i * 22), 6)
                pg.draw.circle(scr, self.PURPLE, (self.pos[0], 42 + self.pos[1] + i * 22), 6)
