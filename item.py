import pygame

class Item:
    def __init__(self, sprite, position, name='Dagger', kind='weapon', slot='hand', stats=[0, 0, 5, 0, 0, 0]):
        self.image = sprite
        self.position = position
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.kind = kind
        self.slot = slot
        self.stats = stats
        self.name = name