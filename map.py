import numpy as np
import pygame
import gfx

class Map:
    def __init__(self, size=(40,40)):
        self.width = size[0]
        self.height = size[1]
        self.tiles = np.zeros(size)
        self.objects = np.zeros(size)
        self.enemies = np.zeros(32)
        self.surface = pygame.Surface((size[0]*16, size[1]*16))

    #Here we can generate something simple, later we can replace this with more complex map generation
    def generateMap(self, rng):
        self.tiles = np.zeros((self.width, self.height))
        
        rooms = rng.integers(3, 9, endpoint=True)

        for i in range(rooms):
            width = rng.integers(5, 10, endpoint=True)
            height = rng.integers(5, 10, endpoint=True)
            xpos = rng.integers(0, self.width-width)
            ypos = rng.integers(0, self.height-height)

            for x in range(xpos, xpos+width):
                for y in range(ypos, ypos+height):
                    self.tiles[x][y] = 1
        
        self.buildSurface()

    #Since maps aren't dynamic right now, we can determine connected tiles and calculate which sprites to use once instead of every frame
    def buildSurface(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.tiles[x][y] > 0:
                    self.surface.blit(gfx.getTileSprite(int(self.tiles[x][y]), self.tiles, (x, y), (self.width, self.height)), (x*16,y*16))

    def draw(self, surf):
        surf.blit(self.surface, (0,0))