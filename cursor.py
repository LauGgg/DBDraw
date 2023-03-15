from text import renderText, getText
from SQLConstants import SQLConstants

class Cursor:
    def __init__(self):
        self.time = 0
        self.pos = (0, 0)
    
    def calculatePos(self, entity):
        if entity.type == SQLConstants.ENTITYSET:
            if entity.state == -1:
                text = getText(entity.name)
                self.pos = (entity.pos[0] + text.get_rect()[2] + 4, entity.pos[1] + 4)
            else:
                text = getText(entity.attributes[entity.state].name)
                self.pos = (entity.pos[0] + text.get_rect()[2] + 4, entity.pos[1] + 9 + (entity.state + 1) * 22)
        else:
            if entity.state == -1:
                text = getText(entity.name, header=True)
                self.pos = (entity.pos[0] + entity.E1.width + entity.space // 2 + text.get_rect()[2] // 2 - 2, entity.pos[1] + 4 + entity.polySize[1] // 2)
            else:
                text = getText(entity.attributes[entity.state].name)
                self.pos = (entity.pos[0] + entity.E1.width + entity.space // 2 + text.get_rect()[2] // 2 - 2, entity.pos[1] - 44)

    def render(self, scr):
        if self.time < 15:
            renderText(scr, "|", self.pos)
        elif self.time == 30:
            self.time = 0
        self.time += 1
