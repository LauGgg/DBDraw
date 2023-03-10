import pygame as pg
from text import renderText
from colors import Colors

class EntitySet(Colors):
    selected = False
    def __init__(self, name, pos, attributes):
        self.name = name
        self.attributes = attributes
        self.pos = pos
    
    def dist(self):
        return 0

    def changeState(self):
        pass

    def addInput(self, inp):
        pass
    
    def render(self, scr, width):
        pg.draw.rect(scr, self.BLUE, (self.pos[0], self.pos[1], width, 29))
        pg.draw.rect(scr, self.BLACK, (self.pos[0], self.pos[1], width, 29), 1)
        pg.draw.rect(scr, self.BLACK, (self.pos[0], self.pos[1], width, 35 + (len(self.attributes) * 22)), 1)
        renderText(scr, self.name, (self.pos[0] + 5, self.pos[1] + 5), header=True)

        for i, attribute in enumerate(self.attributes):
            attribute.render(scr, (self.pos[0] + 5, 32 + self.pos[1] + i * 22))
