import pygame

import mainhandler
from locals import *


class Commons:
    def __init__(self, mainh):
        self.main = mainh

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
        try:
            return self.scrollable
        except:
            return False

    def scroll(self, dir):
        try:
            self.scrool = dir
        except:
            raise ReferenceError

    def calculatesize(self, size):
        wsize = self.main.getwindow().get_size()
        x = (wsize[0] * size[0]) / 100
        y = (wsize[1] * size[1]) / 100
        return x, y

    def setcorrectrectpos(self, rect, pos):
        x, y = pos
        x, y = self.calculatesize((x, y))
        rect = rect.move(x, y)
        return rect


class Scrollbar(Commons):
    def __init__(self, rect):
        self.rect = rect


class Button(Commons):
    def __init__(self, x, y, main, text="", size=(150, 75), clickable=True, color=(255, 255, 255), onclickcallback="",
                 hooverable=True, callbackparameter="", absolutepos=False):
        self.main = main
        self.callbackparameter = callbackparameter
        self.commons = Commons(main)
        self.hooverable = hooverable
        self.ishoovered = False
        self.rect = pygame.Rect(0, 0, size[0], size[1])
        self.window = mainhandler.mainhandler.getwindow(main)
        self.x = x
        self.y = y
        self.color = color
        self.isclickable = clickable and onclickcallback != ""
        if self.isclickable and onclickcallback != "":
            self.onclickcallback = onclickcallback
        self.astext = text != ""
        if self.astext:
            self.text = mainhandler.mainhandler.getfont(self.main).render(text, True, (50, 12, 50))
        self.absolutepos = absolutepos
        if not self.absolutepos:
            if x > 100 or y > 100:
                raise AttributeError

    def show(self):
        self.rect = self.rect.move(-self.rect.left, -self.rect.top)
        if not self.absolutepos:
            self.rect = self.commons.setcorrectrectpos(self.rect, (self.x, self.y))
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


class TextBox(Commons):
    def __init__(self, x, y, main, color=[(255, 255, 255), (211, 211, 211)], size=(250, 150), editable=False,
                 absolutepos=False, autoscroll=True):
        self.commons = Commons(main)
        self.rect = pygame.Rect(0, 0, size[0], size[1])
        self.x = x
        self.y = y
        self.window = mainhandler.mainhandler.getwindow(main)
        self.color = color
        self.editable = editable
        self.textList = []
        self.maximuntextwidth = 0
        while (self.maximuntextwidth < self.rect.width):
            self.maximuntextwidth += FONTSIZE
        self.maximuntextheight = 0
        while (self.maximuntextheight < self.rect.height):
            self.maximuntextheight += FONTSIZE
        self.font = mainhandler.mainhandler.getfont(main)
        self.absolutepos = absolutepos
        if not self.absolutepos:
            if x > 100 or y > 100:
                raise AttributeError
        self.scrollable = autoscroll
        self.scrool = 0

    def show(self):
        self.rect = self.rect.move(-self.rect.left, -self.rect.top)
        if not self.absolutepos:
            self.rect = self.commons.setcorrectrectpos(self.rect, (self.x, self.y))
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
    def __init__(self, img, text, main, size=[150, 100], absolutepos=False):
        self.font = mainhandler.mainhandler.getfont(main)
        self.commons = Commons(main)
        self.img = pygame.transform.scale(pygame.image.load(img), size)
        self.text = text
        self.absolutepos = absolutepos
        self.window = mainhandler.mainhandler.getwindow(main)
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
            self.rect = self.commons.setcorrectrectpos(self.rect, (self.x, self.y))
        else:
            self.rect = self.rect.move(self.x, self.y)
        self.window.blit(self.img, self.rect)
        self.rect = self.rect.move(self.rect.height, 0)
        self.window.blit(self.rendertext(self.text), self.rect)


class ObjectListBox(TextBox):
    def __init__(self, x, y, main, size=[500, 300]):
        self.textbox = TextBox(x, y, main, size=size)
        self.size = size
        self.listshow = self.textbox.show
        self.objlist = []
        self.x = x
        self.y = y

    def show(self):
        self.textbox.show()
        height = 0
        for obj in self.objlist:
            obj.move(self.x, height)
            height += obj.getRect().height
            if height >= self.size[1] and self.textbox.scrollable:
                self.scrollable = True
