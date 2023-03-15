import pygame as pg
from text import renderText

class Attribute:
    def __init__(self, name, primary=False):
        self.name = name
        self.primary = primary

    def render(self, scr, pos, center=False):
        renderText(scr, self.name, pos, underline=self.primary, center=center)
