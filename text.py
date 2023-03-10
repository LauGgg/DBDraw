import pygame as pg

def renderText(scr, text, pos, underline=False, header=False, center=False):
    BLACK = (0, 0, 0)
    if header:
        FONT = pg.font.Font('res/Raleway-Italic.ttf', 18)
    else:
        FONT = pg.font.Font('res/Raleway-LightItalic.ttf', 18)

    text = FONT.render(text, BLACK, True)
    if underline:
        w = text.get_rect()[2]
        pg.draw.line(scr, BLACK, (pos[0], pos[1] + 20), (pos[0] + w, pos[1] + 20), 1)
    if center:
        scr.blit(text, (pos[0] - text.get_rect()[2] // 2, pos[1]))
    else:
        scr.blit(text, pos)
