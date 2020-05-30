import pygame

if not pygame.mixer.get_init():
    pygame.init()

s = pygame.mixer.Sound("1.flac")

s.play()
