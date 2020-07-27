import pygame
from pygame.locals import *
import sys

import panelclass as pnlc
from eventhandler import EventHandler
from locals import *
from mainhandler import mainhandler

pygame.init()
infoObject = pygame.display.Info()
window = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
#window = pygame.display.set_mode((800, 600), HWSURFACE | DOUBLEBUF | RESIZABLE)
def calculuteAbsoluteSize(size):
    return ((infoObject.current_w * size[0]) / 100,(infoObject.current_w * size[1]) / 100)

if pygame.font.get_init():
    font = pygame.font.Font(pygame.font.get_default_font(), FONTSIZE)
running = True
objlist = []
mainh = mainhandler(window, font)
objlist.append(pnlc.ObjectListBox(0,10,mainh,size=calculuteAbsoluteSize((20,90))))
objlist.append(pnlc.ObjectListBox(80,10,mainh,size=calculuteAbsoluteSize((20,90))))
objlist.append(pnlc.ObjectListBox(0,0,mainh,size=calculuteAbsoluteSize((100,10))))

eventhandler = EventHandler(objlist)


def showmousepos(pos):
    text = font.render("x : " + str(pos[0]) + "\n y = " + str(pos[1]), True, (50, 12, 50))
    window.blit(text, pos)


if __name__ == '__main__':
    while running:
        eventhandler.show()
        showmousepos(pygame.mouse.get_pos())
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                eventhandler.click(pygame.mouse.get_pos())
            if event.type == MOUSEWHEEL:
                eventhandler.checkallhover(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
            if event.type == VIDEORESIZE:
                xSize = event.dict['size'][0]
                ySize = event.dict['size'][1]
                screen = pygame.display.set_mode((xSize, ySize), HWSURFACE | DOUBLEBUF | RESIZABLE)

        eventhandler.hoover(pygame.mouse.get_pos())
        window.fill(0)

sys.exit(0)
