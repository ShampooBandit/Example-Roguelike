import pygame
import numpy as np
import actor
import gfx
import map

class Engine:
    def __init__(self):
        self.camera = pygame.Rect(0, 0, 40, 40)
        self.player = actor.Player(gfx.PLAYER_SPRITES[0], (32, 32))
        self.dungeon = map.Map()
        self.rng = np.random.default_rng()
        self.dungeon.generateMap(self.rng)
        self.player.setPosition(self.dungeon.getRandomRoomPosition(self.rng))
        self.dungeon.updateVisible(self.player.position, self.player.vision_radius, self.camera)
        self.updateCamera()

    def handleInput(self, key):
        if key == pygame.K_SPACE:
            self.dungeon.generateMap(self.rng)
            self.player.setPosition(self.dungeon.getRandomRoomPosition(self.rng))
            self.dungeon.updateVisible(self.player.position, self.player.vision_radius, self.camera)
            self.updateCamera()

        took_action = self.player.handleInput(key, self.dungeon)

        if took_action:
            self.dungeon.updateVisible(self.player.position, self.player.vision_radius, self.camera)
            self.updateCamera()
            for e in self.dungeon.enemies:
                e.update()

    def updateCamera(self):
        self.camera[0] = max(0, min(self.player.position[0] - (self.camera[2] / 2), self.dungeon.width - self.camera[2]))
        self.camera[1] = max(0, min(self.player.position[1] - (self.camera[3] / 2), self.dungeon.height - self.camera[3]))

    def draw(self, screen_surface):
        self.dungeon.draw(screen_surface)
        self.player.draw(screen_surface)