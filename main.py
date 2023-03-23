import pygame as pg
from relation import Relation
from entitySet import EntitySet
from attribute import Attribute
from SQLConstants import SQLConstants
from colors import Colors
from cursor import Cursor
from line import Line
from text import renderText
import json

pg.init()

# entities, lines = load("test")

class DBDrawer(SQLConstants):
    entities, lines = [], []
    def __init__(self, w, h) -> None:
        self.w, self.h = w, h
        self.scr = pg.display.set_mode((self.w, self.h), pg.NOFRAME)
        self.bg = pg.Surface((self.w, self.h))
        self.state = self.ENTITY
        self.renderBG()
        self.cursor = Cursor()
        self.clock = pg.time.Clock()
        # self.load("ERDiagramV2")
        self.load("logicaldesign")
        self.entityLoop()
    
    def renderBG(self):
        self.bg.fill(Colors.WHITE)
        for entity in self.entities:
            entity.render(self.bg, self.state)
        for line in self.lines:
            line.render(self.bg)
    
    def route(self):
        if self.state == self.ENTITY:
            self.entityLoop()
        elif self.state == self.LINE:
            self.lineLoop()
        elif self.state == self.SAVE:
            self.save_loop()

    def save_loop(self):
        saveboxw = 200
        run = True
        name = ""
        while run:
            self.scr.fill(Colors.WHITE)
            for event in pg.event.get():
                if event.type == pg.MOUSEMOTION:
                    break
                if event.type == pg.QUIT:
                    run = False
                    self.state = self.END
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        run = False
                        self.state = self.END
                    elif event.key == pg.K_BACKSPACE:
                        if pg.key.get_mods() & pg.KMOD_CTRL:
                            if name == "":
                                self.state = self.ENTITY
                                run = False
                            else:
                                name = ""
                        else:
                            if name != "":
                                name = name[:-1]
                    elif event.key == pg.K_RETURN:
                        if name != "":
                            self.save(name)
                            self.state = self.ENTITY
                            run = False
                    else:
                        key = event.unicode
                        if key:
                            if key.isalpha() or (key.isnumeric() and name != ""):
                                name += key
            self.scr.blit(self.bg, (0, 0))
            pg.draw.rect(self.scr, Colors.BLUE, (self.w // 2 - saveboxw // 2, 40, saveboxw, 50))
            pg.draw.rect(self.scr, Colors.BLACK, (self.w // 2 - saveboxw // 2, 40, saveboxw, 50), 2)
            renderText(self.scr, name, (self.w // 2, 65), center=True)
            renderText(self.scr, "Name:", (self.w // 2, 42), center=True, underline=True, header=True)
            self.clock.tick(30)
            pg.display.update()
        self.route()

    def lineLoop(self):
        run = True
        selected = False
        while run:
            self.scr.fill(Colors.WHITE)
            for event in pg.event.get():
                if event.type == pg.MOUSEMOTION:
                    break
                if event.type == pg.QUIT:
                    run = False
                    self.state = self.END
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        run = False
                        self.state = self.END
                    elif event.key == pg.K_TAB:
                        if pg.key.get_mods() & pg.KMOD_CTRL:
                            if selected:
                                selected.finish()
                            self.state = self.ENTITY
                            run = False
                        else:
                            if selected:
                                pass # tab line
                    elif event.key == pg.K_RETURN:
                        if selected:
                            selected.finish()
                            selected = False
                    elif event.key == pg.K_BACKSPACE:
                        if pg.key.get_mods() & pg.KMOD_CTRL:
                            if selected:
                                self.lines.remove(selected)
                                selected = False
                        else:
                            if selected:
                                selected.deletePoint()
                    elif event.key == pg.K_RIGHT:
                        if selected:
                            pass
                    elif event.key == pg.K_LEFT:
                        if selected:
                            pass
                    elif event.key == pg.K_s and pg.key.get_mods() & pg.KMOD_CTRL:
                        self.state = self.SAVE
                        if selected:
                            selected.finish()
                        run = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    if pg.key.get_mods() & pg.KMOD_CTRL:
                        if selected:
                            selected.finish()
                        for line in self.lines:
                            if line.collide(pos):
                                selected = line
                                line.click()
                                break
                    else:
                        if selected:
                            if selected.addPoint(pos, self.entities):
                                selected = False
                        else:
                            self.lines.append(Line([]))
                            self.lines[-1].addPoint(pos, self.entities)
                            selected = self.lines[-1]
                self.renderBG()
            # if moving[0]:
            #     pos = pg.mouse.get_pos()
            #     selected.move(pos[0] - moving[1][0], pos[1] - moving[1][1])
            #     moving = (True, pos)
            #     self.renderBG()
            self.scr.blit(self.bg, (0, 0))
            self.clock.tick(30)
            pg.display.update()       
        self.route()

    def entityLoop(self):
        run = True
        selected = False
        moving = (False, (0, 0))
        while run:
            self.scr.fill(Colors.WHITE)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    self.state = self.END
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        run = False
                        self.state = self.END
                    elif event.key == pg.K_TAB:
                        if pg.key.get_mods() & pg.KMOD_CTRL:
                            if selected:
                                selected.finish()
                            self.state = self.LINE
                            run = False
                        elif pg.key.get_mods() & pg.KMOD_SHIFT:
                            if selected:
                                selected.tab()
                        else:
                            if selected:
                                selected.writeInput(tab=True)
                    elif event.key == pg.K_RETURN:
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
                                    if selected.type == self.RELATION:
                                        selected.cancelRelation()
                                    self.entities.remove(selected)
                                    selected = False
                        else:
                            if selected:
                                selected.writeInput(delete=1)
                    elif event.key == pg.K_SPACE and pg.key.get_mods() & pg.KMOD_CTRL:
                        if selected:
                            selected.setPrimary()
                    elif event.key == pg.K_RIGHT and selected:
                        if selected.type == self.RELATION:
                            if pg.key.get_mods() & pg.KMOD_CTRL:
                                selected.cycleParticipation(right=True)
                            else:
                                selected.cycleRelation(right=True)
                    elif event.key == pg.K_LEFT and selected:
                        if selected.type == self.RELATION:
                            if pg.key.get_mods() & pg.KMOD_CTRL:
                                selected.cycleParticipation(left=True)
                            else:
                                selected.cycleRelation(left=True)
                    elif event.key == pg.K_w and pg.key.get_mods() & pg.KMOD_CTRL:
                        if selected:
                            selected.cycleWeak()
                    elif event.key == pg.K_s and pg.key.get_mods() & pg.KMOD_CTRL:
                        self.state = self.SAVE
                        if selected:
                            selected.finish()
                        run = False
                    else:
                        if event.unicode.isalpha() or event.unicode.isnumeric() or event.unicode in ['_', '{', '}', '(', ')']:
                            if selected:
                                selected.writeInput(char=event.unicode)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    if pg.key.get_mods() & pg.KMOD_CTRL:
                        if pg.key.get_mods() & pg.KMOD_LSHIFT and selected and selected.type == self.ENTITYSET:
                            selected2 = False
                            for entity in self.entities:
                                if entity.type == self.ENTITYSET and entity.collide(pos):
                                    selected2 = entity
                                    break
                            if selected2:
                                posIndex = 0 if abs(selected.pos[0] - selected2.pos[0]) > abs(selected.pos[1] - selected2.pos[1]) else 1
                                if selected.pos[posIndex] > selected2.pos[posIndex]:
                                    self.entities.append(Relation(selected2, selected, [self.MANY, self.MANY], [self.PARTIAL, self.PARTIAL], []))
                                else:
                                    self.entities.append(Relation(selected, selected2, [self.MANY, self.MANY], [self.PARTIAL, self.PARTIAL], []))
                                selected.finish(), selected2.finish()
                                selected = self.entities[-1]
                        else:
                            if selected:
                                selected.finish()
                                selected = False
                            for entity in self.entities:
                                if entity.collide(pos):
                                    selected = entity
                                    entity.select()
                                    break
                    elif pg.key.get_mods() & pg.KMOD_LSHIFT and selected:
                        moving = (True, pos)
                    else:
                        self.entities.append(EntitySet(pos, 165, attributes=[]))
                        if selected:
                            selected.finish()
                        selected = self.entities[-1]
                elif event.type == pg.MOUSEBUTTONUP:
                    moving = (False, (0, 0))
                self.renderBG()
                if selected:
                    self.cursor.calculatePos(selected)
            if moving[0]:
                pos = pg.mouse.get_pos()
                selected.move(pos[0] - moving[1][0], pos[1] - moving[1][1])
                moving = (True, pos)
                self.renderBG()
            self.scr.blit(self.bg, (0, 0))
            if selected:
                self.cursor.render(self.scr)
            self.clock.tick(30)
            pg.display.update()
        self.route()

    def load(self, name):
        with open(f'saves/json/{name}.json', 'r') as openfile:
            json_object = json.load(openfile)
        self.entities = []
        self.lines = []
        for entityset in json_object['entitysets']:
            self.entities.append(EntitySet(entityset['pos'], 160, entityset['name'], [Attribute(attribute[0], attribute[1]) for attribute in entityset['attributes']]))
            if entityset['weak']:
                self.entities[-1].cycleWeak()
        for relation in json_object['relations']:
            E1, E2 = None, None
            for entity in self.entities:
                if entity.type == SQLConstants.ENTITYSET:
                    if entity.name == relation['entitysetNames'][0]:
                        E1 = entity
                    elif entity.name == relation['entitysetNames'][1]:
                        E2 = entity
            self.entities.append(Relation(E1, E2, relation['relation'], relation['participation'], name=relation['name'], attributes=[Attribute(attribute[0], attribute[1]) for attribute in relation['attributes']]))
            if relation['weak']:
                self.entities[-1].cycleWeak()
        for entity in self.entities:
            entity.finish()
        for line in json_object['lines']:
            l = Line(line['points'])
            if line['arrow']:
                l.arrow = True
            l.finish()
            self.lines.append(l)

    def save(self, name):
        objects = {'entitysets': [], 'relations': [], 'lines': []}
        for entity in self.entities:
            if entity.type == self.ENTITYSET:
                objects['entitysets'].append({
                    'name': entity.name, 
                    'pos': entity.pos, 
                    'attributes': [(attribute.name, attribute.primary) for attribute in entity.attributes],
                    'inRelation': entity.inRelation,
                    'weak': entity.weak
                })
            else:
                objects['relations'].append({
                    'name': entity.name, 
                    'pos': entity.pos, 
                    'attributes': [(attribute.name, attribute.primary) for attribute in entity.attributes], 
                    'weak': entity.weak,
                    'relation': entity.relation,
                    'participation': entity.participation,
                    'entitysetNames': (entity.E1.name, entity.E2.name)
                })
        for line in self.lines:
            objects['lines'].append({
                "points": line.points,
                "arrow": line.arrow
                })
        json_object = json.dumps(objects, indent=4)
        with open(f'saves/json/{name}.json', 'w') as outfile:
            outfile.write(json_object)
        pg.image.save(self.bg, f'saves/img/{name}.png')


if __name__ == "__main__":
    # drawer = DBDrawer(1420, 615)
    drawer = DBDrawer(680, 750)
