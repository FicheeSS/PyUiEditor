import pygame
from pygame.locals import *
import sys

import panelclass as pnlc
from eventhandler import EventHandler
from locals import *
from mainhandler import mainhandler

pygame.init()
infoObject = pygame.display.Info()
# window = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
window = pygame.display.set_mode((800, 600), HWSURFACE | DOUBLEBUF | RESIZABLE)


if pygame.font.get_init():
    font = pygame.font.Font(pygame.font.get_default_font(), FONTSIZE)
running = True
objlist = []
mainh = mainhandler(window, font)
maintextarea = pnlc.TextBox(15, 20, mainh, size=(350, 150))
objlist.append(pnlc.Box(10, 10,mainh, size=(500, 500)))
objlist.append(
    pnlc.Button(30, 50, mainh, text="Button", onclickcallback=maintextarea.addtext, callbackparameter="Non"))
objlist.append(
    pnlc.Button(50, 50, mainh, text="Button", onclickcallback=maintextarea.addtext, callbackparameter="Oui"))
objlist.append(maintextarea)

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
