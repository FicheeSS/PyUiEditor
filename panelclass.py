import pygame

#import mainhandler
from locals import *
from component import *


class Commons:
    def __init__(self, layout):
        self.window = layout.window
        self.layout = layout 

    """Some commons method use by all other class"""

    def getclickable(self):
        """Try to get the obj clickability"""
        try:
            return self.isclickable
        except:
            return False

    def clickcallback(self):
        """Perfom callback on obj"""
        try:
            if self.callbackparameter != "":
                self.onclickcallback(self.callbackparameter)
            else:
                self.onclickcallback()
        except:
            raise ReferenceError

    def getRect(self):
        """Return the pygame.Rect obj from the obj"""
        try:
            return self.rect
        except:
            raise ReferenceError
        
    def getsize(self):
        """Try to get the size of the object """
        try :
            return self.size
        except:
            raise ReferenceError

    def gethooverable(self):
        """Try to get the obj hooverability"""
        try:
            return self.hooverable
        except:
            return False

    def truehoovered(self):
        """Set the hoverability """
        try:
            self.ishoovered = True
        except:
            raise ReferenceError

    def getscrollable(self):
        """Try to get the obj scrollability"""
        try:
            return self.scrollable
        except:
            return False

    def scroll(self, dir):
        """Set the scroll direction"""
        try:
            self.scrool = dir
        except:
            raise ReferenceError

    def calculatesize(self, size):
        """Calculate real size of the obj"""
        wsize = self.layout.size
        x = (wsize[0] * size[0]) / 100
        y = (wsize[1] * size[1]) / 100
        return x, y

    def setrectpos(self, rect, pos):
        """Move the rect in the new corrected position """
        x, y = pos
        x, y = self.calculatesize((x, y))
        rect = rect.move(x, y)
        return rect


class Button(Commons):
    def __init__(self, x, y, layout, text="", size=(150, 75), clickable=True, color=(255, 255, 255), onclickcallback="",
                 hooverable=True, callbackparameter="", absolutepos=False, font=""):
        self.callbackparameter = callbackparameter
        self.commons = Commons(layout)
        self.hooverable = hooverable
        self.ishoovered = False
        self.rect = pygame.Rect(0, 0, size[0], size[1])
        self.window = layout.window
        self.x = x
        self.y = y
        self.color = color
        self.isclickable = clickable and onclickcallback != ""
        self.font = Font(font).getfont()
        if self.isclickable and onclickcallback != "":
            self.onclickcallback = onclickcallback
        self.astext = text != ""
        if self.astext:
            self.text = self.font.render(text, True, (50, 12, 50))
        self.absolutepos = absolutepos
        if not self.absolutepos:
            if x > 100 or y > 100:
                raise AttributeError

    def show(self):
        self.rect = self.rect.move(-self.rect.left, -self.rect.top)
        if not self.absolutepos:
            self.rect = self.commons.setrectpos(self.rect, (self.x, self.y))
        else:
            self.rect = self.rect.move(self.x, self.y)
        if self.ishoovered:
            self.ishoovered = False
            tmpRect = pygame.Rect(self.rect.left - THICKNESS, self.rect.top - THICKNESS,
                                  self.rect.width + THICKNESS * 2, self.rect.height + THICKNESS * 2)
            pygame.draw.rect(self.window, (0, 191, 255), tmpRect)
        else:
            pygame.draw.rect(self.window, self.color, self.rect)
        if self.astext:
            self.window.blit(self.text,
                             (self.rect.left + self.rect.width // 4 + + self.text.get_width() // 2,
                              self.rect.top + self.text.get_height() + self.rect.height // 4))


class Box(Commons):
    def __init__(self, x, y, layout, colorborder=[200,200,200], size=(250, 150),
                 absolutepos=False, autoscroll=True):
        self.commons = Commons(layout)
        self.rect = pygame.Rect(0, 0, size[0], size[1])
        self.x = x
        self.y = y
        self.window = layout.window
        self.bordercolor = colorborder
        self.absolutepos = absolutepos
        if not self.absolutepos:
            if x > 100 or y > 100:
                raise AttributeError
        self.scrollable = autoscroll
        if self.scrollable:
            self.scrooler = Scrollbar(self.rect, self.window)

    def show(self):
        self.rect = self.rect.move(-self.rect.left, -self.rect.top)
        if not self.absolutepos:
            self.rect = self.commons.setrectpos(self.rect, (self.x, self.y))
        else:
            self.rect = self.rect.move(self.x, self.y)
    #draw a rectangle following the box border
        pygame.draw.line(self.window,self.bordercolor,(self.rect.left,self.rect.top),(self.rect.left,self.rect.bottom),2)
        pygame.draw.line(self.window, self.bordercolor, (self.rect.left,self.rect.bottom),(self.rect.right,self.rect.bottom), 2) 
        pygame.draw.line(self.window, self.bordercolor, (self.rect.right,self.rect.bottom),(self.rect.right,self.rect.top), 2)
        pygame.draw.line(self.window, self.bordercolor, (self.rect.right,self.rect.top),(self.rect.left,self.rect.top), 2)


class TextBox(Box):
    def __init__(self, x, y, layout, color=[(255, 255, 255), (211, 211, 211)], size=(250, 150), editable=False,
                 absolutepos=False, autoscroll=True, font=""):
        self.box =Box(x, y, layout, size=size, absolutepos=absolutepos, autoscroll=autoscroll)
        self.rect = pygame.Rect(0, 0, size[0], size[1])
        self.x = x
        self.y = y
        self.window = layout.window 
        self.color = color
        self.editable = editable
        self.textList = []
        self.maximuntextwidth = 0
        self.font = Font(font).getfont()
        while (self.maximuntextwidth < self.rect.width):
            self.maximuntextwidth += FONTSIZE
        self.maximuntextheight = 0
        while (self.maximuntextheight < self.rect.height):
            self.maximuntextheight += FONTSIZE
        self.absolutepos = absolutepos
        if not self.absolutepos:
            if x > 100 or y > 100:
                raise AttributeError
        self.scrollable = autoscroll
        if self.scrollable : 
            self.scrooler = Scrollbar(self.rect, self.window)

    def show(self):
        self.rect = self.rect.move(-self.rect.left, -self.rect.top)
        if not self.absolutepos:
            self.rect = self.box.commons.setrectpos(self.rect, (self.x, self.y))
        else:
            self.rect = self.rect.move(self.x, self.y)
        if self.editable:
            pygame.draw.rect(self.window, self.color[1], self.rect)
        else:
            pygame.draw.rect(self.window, self.color[0], self.rect)
        if len(self.textList) != 0:
            for i in range(len(self.textList)):
                text = self.font.render(str(self.textList[i]), True, (50, 12, 50))
                self.window.blit(text,
                                 (self.rect.left,
                                  self.rect.top + text.get_height() * i))
        if self.scrollable:
            pass

    def listtostring(self, charlist):
        """Transform a list of char into a string"""
        s = ""
        for char in charlist:
            s += char
        return s

    def addtext(self, text):
        """Add text to the be showed"""
        index = 0
        tmp = []
        while index < len(text):
            tmp.append(text[index])
            index += 1
            if index % (self.maximuntextwidth // FONTSIZE * 2) == 0:
                self.textList.append(self.listtostring(tmp))
                tmp = []
        self.textList.append(self.listtostring(tmp))
        dif = len(self.textList) - self.maximuntextheight // FONTSIZE + 2
        if dif > 0:
            for i in range(dif):
                self.textList.pop(i)


class BoxElement(Commons):
    def __init__(self, imgPath, text, layout, size=[150, 100], absolutepos=False, font=""):
        self.commons = Commons(layout)
        self.font = Font(font).getfont()
        self.img = pygame.transform.scale(pygame.image.load(imgPath), size)
        self.text = text
        self.absolutepos = absolutepos
        self.window = layout.window
        self.x = 0
        self.y = 0
        self.size = size
        self.rect = pygame.Rect((self.x, self.y), size)

    def rendertext(self, text):
        return self.font.render(text, True, (50, 12, 50))

    def move(self, pos):
        self.rect = pygame.Rect(pos, self.size)

    def show(self):
        self.rect = self.rect.move(-self.rect.left, -self.rect.top)
        if not self.absolutepos:
            self.rect = self.commons.setrectpos(self.rect, (self.x, self.y))
        else:
            self.rect = self.rect.move(self.x, self.y)
        self.window.blit(self.img, self.rect)
        self.rect = self.rect.move(self.rect.height, 0)
        self.window.blit(self.rendertext(self.text), self.rect)


class ObjectListBox(Box):
    def __init__(self, x, y, layout, size=[500, 300], scrollable=True,  absolutepos=False):
        self.box = Box(x, y, layout, size=size, autoscroll=scrollable,  absolutepos=absolutepos)
        self.rect = self.box.rect 
        self.size = size
        self.layout = layout
        self.objlist = []
        self.x = x 
        self.y = y
        if scrollable : 
            self.scroller = self.box.scrooler
        self.scrollable = scrollable
        self.absolutepos = absolutepos


    def addImg(self, imgPath, text):
        self.objlist.append(BoxElement(imgPath, text, self.layout, absolutepos=self.absolutepos))
        print(str(self.objlist) + " Current objlen = " + str(len(self.objlist)) + " current obj = " + str(self))
        
    def show(self):
        self.box.show()
        height = 0
        for obj in self.objlist:
            obj.move((self.x, height))
            height += obj.getRect().height
            if height >= self.size[1]:
                if self.box.scrollable:
                    self.scrollable = True
                else:
                    raise AttributeError
            if self.scrollable and height > self.size[1]:
                self.scrooler.show()
                
    def getobjlist(self):
        #debug
        return self.objlist
    
