import pygame

pygame.init()

screen = pygame.display.set_mode((1280, 720), pygame.HWSURFACE)
screen_surface = screen.copy()
screen_scale = (screen.get_width() * 1, screen.get_height() * 1)
clock = pygame.time.Clock()
font = pygame.font.Font('gfx/GUI/SDS_8x8.ttf', 16)

import engine
running = True

game_engine = engine.Engine()

while running:
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                running = False
            case pygame.KEYDOWN:
                game_engine.handleInput(event.key)
            case _:
                pass

    screen_surface.fill(pygame.Color(0,30,30))

    game_engine.draw(screen_surface, font)

    screen.blit(pygame.transform.scale(screen_surface, screen_scale), (0,0))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()