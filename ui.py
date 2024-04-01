import pygame
import gfx

class GUI:
    def __init__(self):
        self.inv_window = gfx.GUI_BOX_SPRITES[0]
        self.game_border_rect = pygame.Rect(315, 35, 672, 672)
        self.game_border = pygame.surface.Surface((672, 672), pygame.SRCALPHA)
        self.buildGameBorder()

    def buildGameBorder(self):
        self.game_border.blit(gfx.GUI_BOX_SPRITES[0], (0, 0))
        for x in range(19):
            self.game_border.blit(gfx.GUI_BOX_SPRITES[4], (32 + (x*32), 0))
            self.game_border.blit(gfx.GUI_BOX_SPRITES[7], (32 + (x*32), 618))
        for y in range(19):
            self.game_border.blit(gfx.GUI_BOX_SPRITES[5], (0, 32 + (y*32)))
            self.game_border.blit(gfx.GUI_BOX_SPRITES[6], (618, 32 + (y*32)))
        self.game_border.blit(gfx.GUI_BOX_SPRITES[1], (618, 0))
        self.game_border.blit(gfx.GUI_BOX_SPRITES[2], (0, 618))
        self.game_border.blit(gfx.GUI_BOX_SPRITES[3], (618, 618))

    def draw(self, surface):
        surface.blit(self.game_border, self.game_border_rect)