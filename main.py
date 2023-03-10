import pygame as pg
from relation import Relation
from entitySet import EntitySet
from attribute import Attribute
from SQLConstants import SQLConstants
from colors import Colors

pg.init()

cars = EntitySet("car", (100, 100), [Attribute("license_no", True), Attribute("owner"), Attribute("model")])
services = EntitySet("services", (400, 400), [Attribute("service_no", True), Attribute("type"), Attribute("price")])
entitySets = [cars, services]
relations = [Relation(cars, services, (SQLConstants.ONE, SQLConstants.MANY), (200, 200), attributes = [Attribute("date"), Attribute("hours")], name="repair")]

# entitySets = []
# relations = []

w, h = 1000, 600
scr = pg.display.set_mode((w, h))

def renderBG():
    bg = pg.Surface((w, h))
    bg.fill(Colors.WHITE)
    for relation in relations:
        relation.render(bg)
    for entitySet in entitySets:
        entitySet.render(bg, 120)
    return bg

bg = renderBG()

selected = 0
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
                entitySets[-1].tabbed()
                pass
            else:
                print(event.unicode)
                entitySets[-1].name += event.unicode
                bg = renderBG()
        elif event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            print("something")
            entitySets.append(EntitySet("", pos, []))
            bg = renderBG()
        elif event.type == pg.MOUSEBUTTONUP:
            pass

    scr.blit(bg, (0, 0))
    pg.display.update()

