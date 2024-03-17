import pygame

class Actor:
    def __init__(self, sprite, position):
        self.sprite = sprite
        self.position = position

    def draw(self, surface):
        surface.blit(self.sprite, self.position)

class Player(Actor):
    def handleInput(self, key):
        return False