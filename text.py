import pygame as pg
from colors import Colors


def renderText(scr, text, pos, underline=False, header=False, center=False):
    if header:
        FONT = pg.font.Font('res/Raleway-Italic.ttf', 18)
    else:
        FONT = pg.font.Font('res/Raleway-LightItalic.ttf', 18)
    text = FONT.render(text, Colors.BLACK, True)
    if underline:
        rect = text.get_rect()
        if center:
            pg.draw.line(scr, Colors.BLACK, (pos[0] - rect[2] // 2, pos[1] + 20), (pos[0] + rect[2] - rect[2] // 2, pos[1] + 20), 1)
        else:
            pg.draw.line(scr, Colors.BLACK, (pos[0], pos[1] + 20), (pos[0] + rect[2], pos[1] + 20), 1)
    if center:
        scr.blit(text, (pos[0] - text.get_rect()[2] // 2, pos[1]))
    else:
        scr.blit(text, pos)


def getText(text, header=False):
    if header:
        FONT = pg.font.Font('res/Raleway-Italic.ttf', 18)
    else:
        FONT = pg.font.Font('res/Raleway-LightItalic.ttf', 18)
    return FONT.render(text, Colors.BLACK, True)

