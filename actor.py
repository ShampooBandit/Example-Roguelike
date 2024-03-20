import pygame

class Actor(pygame.sprite.Sprite):
    def __init__(self, sprite, position):
        super().__init__()
        self.image = sprite
        self.position = position
        self.rect = pygame.Rect(position[0] * 16, position[1] * 16, 16, 16)
        self.vision_radius = 6
        self.equipment = {
            'Left Hand': None,
            'Right Hand': None,
            'Left Ring Finger': None,
            'Right Ring Finger': None,
            'Head': None,
            'Neck': None,
            'Torso': None,
            'Legs': None,
            'Feet': None
        }
        #Stats in order of HP, MP, Strength, Defence, Intelligence, Agility
        self.base_stats = [10, 0, 3, 2, 2, 2]
        self.current_stats = [10, 0, 3, 2, 2, 2]
        self.inventory = []

    def update(self):
        pass

    def setPosition(self, position):
        self.position = position

    def adjustToCamera(self, camera):
        self.rect[0] = (self.position[0] - camera[0]) * 16 + 320
        self.rect[1] = (self.position[1] - camera[1]) * 16 + 32

class Player(Actor):
    def __init__(self, sprite, position):
        super().__init__(sprite, position)
        self.base_stats = [25, 0, 3, 2, 2, 2]
        self.current_stats = [25, 0, 3, 2, 2, 2]

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
            case pygame.K_KP_ENTER | pygame.K_RETURN:
                item = dungeon.pickupItemAtTile(self.position)
                if item:
                    self.inventory.append(item)
                    action = 'pickup'
                    self.autoEquip(self.inventory[-1])
        
        return action
    
    def autoEquip(self, item):
        match item.slot:
            case 'hand':
                if self.equipment['Left Hand'] == None:
                    self.equipment['Left Hand'] = item
                elif self.equipment['Right Hand'] == None:
                    self.equipment['Right Hand'] = item
        self.updateStats()

    def updateStats(self):
        self.current_stats = self.base_stats.copy()
        for value in self.equipment.values():
            if value:
                i = 0
                for stat in value.stats:
                    self.current_stats[i] += stat
                    i += 1
    
    def draw(self, surface, font):
        y = 32
        for k, v in self.equipment.items():
            if v:
                text = font.render(k + ' ' + v.name, False, pygame.Color('white'))
            else:
                text = font.render(k + ' None', False, pygame.Color('white'))
            surface.blit(text, (0, y))
            y += 16

        y += 16
        for n in self.current_stats:
            text = font.render(str(n), False, pygame.Color('white'))
            surface.blit(text, (0, y))
            y += 16

        y = 32
        for i in self.inventory:
            text = font.render(i.name, False, pygame.Color('white'))
            surface.blit(text, (1000, y))
            y += 16
        surface.blit(self.image, self.rect)
    
class Enemy(Actor):
    def update(self):
        pass