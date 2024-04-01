import pygame
import math

class Actor(pygame.sprite.Sprite):
    def __init__(self, sprite, position):
        super().__init__()
        self.image = sprite
        self.position = position
        self.rect = pygame.Rect(position[0] * 16, position[1] * 16, 16, 16)
        self.vision_radius = 8
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
        #Stats in order of HP, MP, Strength, Defence, Intelligence, Mind, Agility, Luck
        self.base_stats = [10, 0, 1, 1, 1, 1, 1, 1]
        self.current_stats = [10, 0, 1, 1, 1, 1, 1, 1]
        self.inventory = []
        self.skills = {}
        self.name = ''

    def update(self):
        pass

    def setPosition(self, position):
        self.position = position

    def adjustToCamera(self, camera):
        self.rect[0] = (self.position[0] - camera[0]) * 16 + 320
        self.rect[1] = (self.position[1] - camera[1]) * 16 + 40

    def attackTarget(self, target, rng):
        if self.rollToHit(target, rng):
            dmg_mult = rng.integers(80, 120)
            base_dmg = self.current_stats[2] - target.current_stats[3]
            dmg = math.ceil(base_dmg * (dmg_mult / 100))
            target.current_stats[0] -= dmg
            return (str(target.name), str(dmg))
        else:
            return (str(target.name), 'miss')

    def rollToHit(self, target, rng):
        roll = rng.integers(0, 100) + (self.current_stats[7] / 2)
        dv = (self.current_stats[6] / target.current_stats[6]) * 100
        return (roll <= dv)
    
    def updateStats(self):
        self.current_stats = self.base_stats.copy()
        for value in self.equipment.values():
            if value:
                i = 0
                for stat in value.stats:
                    self.current_stats[i] += stat
                    i += 1

class Player(Actor):
    def __init__(self, sprite, position):
        super().__init__(sprite, position)
        self.base_stats = [25, 10, 1, 1, 1, 1, 1, 1]
        self.current_stats = [25, 10, 1, 1, 1, 1, 1, 1]
        self.bag_size = 10
        self.name = 'Player'

    def handleInput(self, key, dungeon, rng):
        action = ''
        info = ''
        match key:
            case pygame.K_a | pygame.K_LEFT:
                enemy = dungeon.checkEnemyAtTile(self.position[0]-1, self.position[1])
                if enemy:
                    action = 'attack'
                    info = self.attackTarget(enemy, rng)
                elif not dungeon.checkSolid(self.position[0]-1, self.position[1]):
                    action = 'left'
                    self.setPosition((self.position[0] - 1, self.position[1]))
            case pygame.K_d | pygame.K_RIGHT:
                enemy = dungeon.checkEnemyAtTile(self.position[0]+1, self.position[1])
                if enemy:
                    action = 'attack'
                    info = self.attackTarget(enemy, rng)
                elif not dungeon.checkSolid(self.position[0]+1, self.position[1]):
                    action = 'right'
                    self.setPosition((self.position[0] + 1, self.position[1]))
            case pygame.K_w | pygame.K_UP:
                enemy = dungeon.checkEnemyAtTile(self.position[0], self.position[1]-1)
                if enemy:
                    action = 'attack'
                    info = self.attackTarget(enemy, rng)
                elif not dungeon.checkSolid(self.position[0], self.position[1]-1):
                    action = 'up'
                    self.setPosition((self.position[0], self.position[1] - 1))
            case pygame.K_s | pygame.K_DOWN:
                enemy = dungeon.checkEnemyAtTile(self.position[0], self.position[1]+1)
                if enemy:
                    action = 'attack'
                    info = self.attackTarget(enemy, rng)
                elif not dungeon.checkSolid(self.position[0], self.position[1]+1):
                    action = 'down'
                    self.setPosition((self.position[0], self.position[1] + 1))
            case pygame.K_KP_ENTER | pygame.K_RETURN:
                item = dungeon.pickupItemAtTile(self.position[0], self.position[1])
                if item:
                    self.inventory.append(item)
                    action = 'pickup'
                    self.autoEquip(self.inventory[-1])
        
        return action, info
    
    def autoEquip(self, item):
        match item.slot:
            case 'hand':
                if self.equipment['Left Hand'] == None:
                    self.equipment['Left Hand'] = item
                elif self.equipment['Right Hand'] == None:
                    self.equipment['Right Hand'] = item
        self.updateStats()
    
    def draw(self, surface, font):
        surface.blit(self.image, self.rect)
    
class Enemy(Actor):
    def __init__(self, sprite, position):
        super().__init__(sprite, position)
        self.state = 'idle'
        self.destination = None
        self.name = 'Bug'

    def update(self):
        match self.state:
            case 'idle':
                pass