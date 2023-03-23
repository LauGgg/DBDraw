import pygame as pg
from colors import Colors


def renderText(scr, text, pos, underline=False, header=False, center=False, stipled=False, font_size=18):
    if header:
        FONT = pg.font.Font('res/Raleway-Italic.ttf', font_size)
    else:
        FONT = pg.font.Font('res/Raleway-LightItalic.ttf', font_size)
    text = FONT.render(text, Colors.BLACK, True)
    if underline:
        rect = text.get_rect()
        if center:
            if stipled:
                pass
            else:
                pg.draw.line(scr, Colors.BLACK, (pos[0] - rect[2] // 2, pos[1] + 20), (pos[0] + rect[2] - rect[2] // 2, pos[1] + 20), 1)
        else:
            if stipled:
                dots = text.get_rect()[2] // 14
                for i in range(dots * 2 + 1):
                    if i % 2 == 0:
                        pg.draw.line(scr, Colors.BLACK, (pos[0] + 7 * i, pos[1] + 20), (pos[0] + (7 * (i + 1)) + 3, pos[1] + 20), 1)
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

