import pygame

class Tile:
    def __init__(self, id):
        self.id = id
        self.sprite = pygame.Surface((16,16))

    def checkNeighbors(self, map):
        self.updateSprite()

    def updateSprite(self):
        pass