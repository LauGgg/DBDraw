import pygame as pg
from relation import Relation
from entitySet import EntitySet
from attribute import Attribute
from SQLConstants import SQLConstants
from colors import Colors
from cursor import Cursor
from line import Line

pg.init()

# cars = EntitySet("car", (100, 100), [Attribute("license_no", True), Attribute("owner"), Attribute("model")])
# services = EntitySet("services", (400, 400), [Attribute("service_no", True), Attribute("type"), Attribute("price")])
# entitySets = [cars, services]
# relations = [Relation(cars, services, (SQLConstants.ONE, SQLConstants.MANY), (200, 200), attributes = [Attribute("date"), Attribute("hours")], name="repair")]

entitys = [] # entitysets and relations
lines = [Line([(200, 50), (300, 50), (300, 100)]), Line([(500, 500)])]


def renderBG():
    bg = pg.Surface((w, h))
    bg.fill(Colors.WHITE)
    for entity in entitys:
        entity.render(bg)
    for line in lines:
        line.render(bg)
    return bg


w, h = 1000, 600
scr = pg.display.set_mode((w, h))
bg = renderBG()
moving = (False, (0, 0))
cursor = Cursor()
clock = pg.time.Clock()
selected = False
state = SQLConstants.ENTITY

run = True
while run:
    scr.fill(Colors.WHITE)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                run = False
            elif event.key == pg.K_TAB:
                if state == SQLConstants.ENTITY:
                    state = SQLConstants.LINE
                    selected = False
                else:
                    state = SQLConstants.ENTITY
                    selected = False
            elif event.key == pg.K_RETURN:
                if state == SQLConstants.ENTITY:
                    if pg.key.get_mods() & pg.KMOD_CTRL:
                        if selected:
                            selected.finish()
                            selected = False                 
                    else:
                        if selected:
                            selected.addAttribute()
            elif event.key == pg.K_BACKSPACE:
                if pg.key.get_mods() & pg.KMOD_CTRL:
                    if selected:
                        if selected.writeInput(delete=2):
                            entitys.pop(selected)
                            selected = False
                else:
                    if selected:
                        selected.writeInput(delete=1)
            elif event.key == pg.K_SPACE and pg.key.get_mods() & pg.KMOD_CTRL:
                if selected:
                    selected.setPrimary()
            else:
                if event.unicode.isalpha():
                    if selected:
                        selected.writeInput(char=event.unicode)
        elif event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            if pg.key.get_mods() & pg.KMOD_CTRL:
                if pg.key.get_mods() & pg.KMOD_LSHIFT and selected and selected.type == SQLConstants.ENTITYSET:
                    selected2 = False
                    for entity in entitys:
                        if entity.type == SQLConstants.ENTITYSET and entity.collide(pos):
                            selected2 = entity
                            break
                    if selected2:
                        if selected.pos[0] > selected2.pos[0]:
                            entitys.append(Relation(selected2, selected, (SQLConstants.MANY, SQLConstants.MANY)))
                        else:
                            entitys.append(Relation(selected, selected2, (SQLConstants.MANY, SQLConstants.MANY)))
                        selected.finish(), selected2.finish()
                        selected = entitys[-1]
                else:
                    if selected:
                        selected.finish()
                        selected = False
                    for entity in entitys:
                        if entity.collide(pos):
                            selected = entity
                            entity.select()
                            break
                    # print("found none")
            elif pg.key.get_mods() & pg.KMOD_LSHIFT and selected:
                moving = (True, pos)
            else:
                entitys.append(EntitySet(pos, 120))
                if selected:
                    selected.finish()
                selected = entitys[-1]
        elif event.type == pg.MOUSEBUTTONUP:
            moving = (False, (0, 0))
        bg = renderBG()
        if selected:
            cursor.calculatePos(selected)
    if moving[0]:
        pos = pg.mouse.get_pos()
        selected.move(pos[0] - moving[1][0], pos[1] - moving[1][1])
        moving = (True, pos)
        bg = renderBG()

    scr.blit(bg, (0, 0))
    if selected:
        cursor.render(scr)
    clock.tick(30)
    pg.display.update()

