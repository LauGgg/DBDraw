from attribute import Attribute

class DBRender():
    def __init__(self, pos, type, name="", attributes=[]):
        self.pos = pos
        self.name = name
        self.type = type
        self.attributes = attributes
        self.selected = True
        self.state = len(self.attributes) - 1
        self.weak = False
    
    def tab(self):
        if self.state == len(self.attributes) - 1:
            self.state = -1
        else:
            self.state += 1
    
    def addAttribute(self):
        self.attributes.append(Attribute("", False))
        self.state = len(self.attributes) - 1
    
    def setPrimary(self):
        if self.state != -1:
            self.attributes[self.state].primary = not self.attributes[self.state].primary
    
    def finish(self):
        self.selected = False
    
    def select(self):
        self.selected = True
        
    def cycleWeak(self):
        self.weak = not self.weak
    
    def writeInput(self, char="", delete=0, tab=False):
        if tab:
            if self.state == -1:
                self.name += "    "
            else:
                self.attributes[self.state].name += "    "

        # print(char)
        if self.state == -1:
            if delete == 1:
                self.name = self.name[:-1]
            elif delete == 2:
                if self.name == "":
                    return True
                self.name = ""
            else:
                self.name += char
        else:
            if delete == 1:
                self.attributes[self.state].name = self.attributes[self.state].name[:-1]
            elif delete == 2:
                if self.attributes[self.state].name == "":
                    self.attributes.pop(self.state)
                    self.state -= 1
                else:
                    self.attributes[self.state].name = ""
            else:
                self.attributes[self.state].name += char
        return False

    