import pygame
import numpy as np
import actor
import gfx
import map
import ui

class Engine:
    def __init__(self):
        self.repeat_timer = -1
        self.repeat_key = -1
        self.camera = pygame.Rect(0, 0, 40, 40)
        self.player = actor.Player(gfx.PLAYER_SPRITES[0], (32, 32))
        self.dungeon = map.Map()
        self.gui = ui.GUI()
        self.rng = np.random.default_rng()
        self.dungeon.generateMap(self.rng)
        self.player.setPosition(self.dungeon.getRandomRoomPosition(self.rng))
        self.updateCamera()
        self.dungeon.updateVisible(self.player.position, self.player.vision_radius, self.camera)

    def handleInput(self, key):
        if key == pygame.K_SPACE:
            self.dungeon.generateMap(self.rng)
            self.player.setPosition(self.dungeon.getRandomRoomPosition(self.rng))
            self.updateCamera()
            self.dungeon.updateVisible(self.player.position, self.player.vision_radius, self.camera)
        
        self.repeat_timer = 20
        self.repeat_key = key

        self.handlePlayerAction(key)

    def handlePlayerAction(self, key):
        took_action = self.player.handleInput(key, self.dungeon, self.rng)

        if took_action:
            self.updateCamera()
            for e in self.dungeon.all_enemies:
                e.update()
                e.adjustToCamera(self.camera)
            self.dungeon.updateVisible(self.player.position, self.player.vision_radius, self.camera)

    def updateCamera(self):
        self.camera[0] = max(0, min(self.player.position[0] - (self.camera[2] / 2), self.dungeon.width - self.camera[2]))
        self.camera[1] = max(0, min(self.player.position[1] - (self.camera[3] / 2), self.dungeon.height - self.camera[3]))
        self.player.adjustToCamera(self.camera)

    def update(self):
        if not self.repeat_timer == -1:
            self.repeat_timer -= 1
            if self.repeat_timer == 0:
                self.repeat_timer = 3
                self.handlePlayerAction(self.repeat_key)

    def clearRepeatTimer(self, key):
        if key == self.repeat_key:
            self.repeat_timer = -1
            self.repeat_key = -1

    def draw(self, screen_surface, font):
        self.gui.draw(screen_surface)
        self.dungeon.draw(screen_surface)
        self.dungeon.visible_enemies.draw(screen_surface)
        self.player.draw(screen_surface, font)