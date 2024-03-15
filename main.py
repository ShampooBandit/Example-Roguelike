import pygame
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((1280, 720), HWSURFACE)
screen_surface = screen.copy()
screen_scale = (screen.get_width() * 1, screen.get_height() * 1)
clock = pygame.time.Clock()
font = pygame.font.SysFont('lucida console', 16)

import engine

running = True
keyboard = {}

game_engine = engine.Engine()

while running:
    keyboard = pygame.key.get_pressed()

    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                running = False
            case pygame.KEYDOWN:
                game_engine.handleInput(keyboard)
            case _:
                pass

    screen_surface.fill(pygame.Color(0,30,30))

    game_engine.draw(screen_surface)

    screen.blit(pygame.transform.scale(screen_surface, screen_scale), (0,0))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()