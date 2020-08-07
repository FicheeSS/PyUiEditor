from locals import *

import pygame


class Scrollbar:
    def __init__(self, rect, window):
        self.rect = rect
        self.window = window
        self.rectduet = (
        pygame.Rect(self.rect.left + self.rect.width - SCROLLBARWIDTH, self.rect.top, SCROLLBARWIDTH, self.rect.height),
        pygame.Rect(self.rect.left + self.rect.width - SCROLLBARWIDTH, self.rect.top, SCROLLBARWIDTH,
                    self.rect.height - 1))
        

    def updatescrolldong(self,rect, size , csize):
        height = size-(csize-size)
        return pygame.Rect(rect.top, rect.left, rect.width, height)


    def updatescrollbar(self, size, csize):
        if size > csize : 
            pass
        else:
            self.rectduet[1] = self.updatescrolldong(self.rectduet[1], size, csize)

            

    def show(self):
        pass

class Font():
    def __init__(self, font=""):
        if not not font :
            self.font = DEFAULTFONT
        else :
            f = pygame.font.match_font(font)
            if f == None:
                self.font = DEFAULTFONT
            else : 
                self.font = f
            
    def getfont(self):
        return self.font