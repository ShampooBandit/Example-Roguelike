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
            self.updateCamera()
            self.dungeon.updateVisible(self.player.position, self.player.vision_radius, self.camera)
            for e in self.dungeon.enemies:
                e.update()

    def updateCamera(self):
        self.camera[0] = max(0, min(self.player.position[0] - (self.camera[2] / 2), self.dungeon.width - self.camera[2]))
        self.camera[1] = max(0, min(self.player.position[1] - (self.camera[3] / 2), self.dungeon.height - self.camera[3]))
        self.player.adjustToCamera(self.camera)

    def draw(self, screen_surface, font):
        self.dungeon.draw(screen_surface)
        self.player.draw(screen_surface)

        text1 = font.render('Camera x: ' + str(self.camera[0]), False, pygame.Color(255,255,255))
        text2 = font.render('Camera y: ' + str(self.camera[1]), False, pygame.Color(255,255,255))

        text3 = font.render('Player x: ' + str(self.player.position[0]), False, pygame.Color(255,255,255))
        text4 = font.render('Player y: ' + str(self.player.position[1]), False, pygame.Color(255,255,255))

        screen_surface.blit(text1, (0, 0))
        screen_surface.blit(text2, (0, 16))
        screen_surface.blit(text3, (0, 32))
        screen_surface.blit(text4, (0, 48))