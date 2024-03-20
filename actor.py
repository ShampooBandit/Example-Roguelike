import pygame

class Actor(pygame.sprite.Sprite):
    def __init__(self, sprite, position):
        super().__init__()
        self.image = sprite
        self.position = position
        self.rect = pygame.Rect(position[0] * 16, position[1] * 16, 16, 16)
        self.vision_radius = 4

    def update(self):
        pass

    def setPosition(self, position):
        self.position = position
        self.rect[0] = position[0] * 16
        self.rect[1] = position[1] * 16

class Player(Actor):
    def handleInput(self, key, dungeon):
        action = ''
        match key:
            case pygame.K_a | pygame.K_LEFT:
                if dungeon.checkValidTile((self.position[0]-1, self.position[1])):
                    action = 'left'
                    self.setPosition((self.position[0] - 1, self.position[1]))
            case pygame.K_d | pygame.K_RIGHT:
                if dungeon.checkValidTile((self.position[0]+1, self.position[1])):
                    action = 'right'
                    self.setPosition((self.position[0] + 1, self.position[1]))
            case pygame.K_w | pygame.K_UP:
                if dungeon.checkValidTile((self.position[0], self.position[1]-1)):
                    action = 'up'
                    self.setPosition((self.position[0], self.position[1] - 1))
            case pygame.K_s | pygame.K_DOWN:
                if dungeon.checkValidTile((self.position[0], self.position[1]+1)):
                    action = 'down'
                    self.setPosition((self.position[0], self.position[1] + 1))
        
        return action
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
class Enemy(Actor):
    def update(self):
        pass