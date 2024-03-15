import pygame
import numpy as np
import actor
import gfx
import map

class Engine:
    def __init__(self):
        self.player = actor.Player(gfx.PLAYER_SPRITES[0], (32, 32))
        self.dungeon = map.Map()
        self.rng = np.random.default_rng()
        self.dungeon.generateMap(self.rng)

    def handleInput(self, keyboard):
        self.player.handleInput(keyboard)

    def draw(self, screen_surface):
        self.dungeon.draw(screen_surface)
        self.player.draw(screen_surface)