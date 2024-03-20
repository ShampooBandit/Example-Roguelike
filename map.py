import numpy as np
import pygame
import gfx
import actor

class Map:
    def __init__(self, size=(120,120)):
        self.width = size[0]
        self.height = size[1]
        self.tiles = np.zeros(size, dtype=int)
        self.objects = np.zeros(size, dtype=int)
        self.visible = np.zeros(size, dtype=bool)
        self.memory = np.zeros(size, dtype=bool)
        self.solid = np.ones(size, dtype=bool)
        #self.enemies = pygame.sprite.Group()
        self.enemies = np.zeros(size, dtype=object)
        self.all_enemies = pygame.sprite.Group()
        self.visible_enemies = pygame.sprite.Group()
        self.rooms = []

    #Here we can generate something simple, later we can replace this with more complex map generation
    def generateMap(self, rng):
        self.__init__()

        room_count = rng.integers(5, 15, endpoint=True)

        #Create and position the rooms
        for i in range(room_count):
            width = rng.integers(5, 20, endpoint=True)
            height = rng.integers(5, 20, endpoint=True)
            xpos = rng.integers(0, self.width-width)
            ypos = rng.integers(0, self.height-height)
            self.rooms.append(pygame.Rect(xpos, ypos, width, height))

            self.tiles[xpos:xpos+width, ypos:ypos+height] = 1
            self.solid[xpos:xpos+width, ypos:ypos+height] = 0

        #Connect all the rooms with hallways
        for i in range(room_count):
            if i < (room_count-1):
                if self.rooms[i][0] < self.rooms[i+1][0]:
                    x1 = self.rooms[i][0] + self.rooms[i][2]
                    x2 = rng.integers(self.rooms[i+1][0] + 1, self.rooms[i+1][0] + self.rooms[i+1][2])
                else:
                    x1 = self.rooms[i][0]
                    x2 = rng.integers(self.rooms[i+1][0] + 1, self.rooms[i+1][0] + self.rooms[i+1][2])

                if self.rooms[i][1] < self.rooms[i+1][1]:
                    y1 = rng.integers(self.rooms[i][1] + 1, self.rooms[i][1] + self.rooms[i][3])
                    y2 = self.rooms[i+1][1]
                else:
                    y1 = rng.integers(self.rooms[i][1] + 1, self.rooms[i][1] + self.rooms[i][3])
                    y2 = self.rooms[i+1][1] + self.rooms[i+1][3]

                self.tiles[min(x1,x2):max(x1,x2),y1] = 1
                self.tiles[x2,min(y1,y2):max(y1,y2)] = 1
                self.tiles[x2][y1] = 1
                self.solid[min(x1,x2):max(x1,x2),y1] = 0
                self.solid[x2,min(y1,y2):max(y1,y2)] = 0
                self.solid[x2][y1] = 0

        #Generate some enemies to add to rooms
        enemy_count = rng.integers(room_count, room_count + 10)
        for i in range(enemy_count):
            pos = self.getRandomRoomPosition(rng)
            self.enemies[pos[0]][pos[1]] = actor.Enemy(gfx.MONSTER_SPRITES[0], pos)
            self.all_enemies.add(self.enemies[pos[0]][pos[1]])
            self.solid[pos[0]][pos[1]] = 1

    #Stitch together the visible tiles to render to the screen
    def buildSurface(self, camera):
        self.surface = pygame.Surface((camera[2] * 16, camera[3] * 16))
        self.visible_enemies.empty()
        
        for x in range(0, camera[2]):
            xpos = camera[0] + x
            for y in range(0, camera[3]):
                ypos = camera[1] + y
                if self.tiles[xpos][ypos] > 0:
                    if self.visible[xpos][ypos]:
                        self.surface.blit(gfx.getTileSprite(self.tiles[xpos][ypos], self.tiles, (xpos, ypos), (self.width, self.height)), (x * 16, y * 16))
                        if self.enemies[xpos][ypos]:
                            self.visible_enemies.add(self.enemies[xpos][ypos])
                    elif self.memory[xpos][ypos]:
                        tile = gfx.getTileSprite(self.tiles[xpos][ypos], self.tiles, (xpos, ypos), (self.width, self.height))
                        tile = pygame.transform.grayscale(tile)
                        self.surface.blit(tile, (x * 16, y * 16))

    def updateVisible(self, position, radius, camera):
        self.visible = np.zeros((self.width, self.height), dtype=bool)

        x1 = max(position[0] - radius, 0)
        x2 = min(position[0] + radius + 1, self.width - 1)
        y1 = max(position[1] - radius, 0)
        y2 = min(position[1] + radius + 1, self.height - 1)

        self.visible[x1:x2, y1:y2] = 1
        self.memory[x1:x2, y1:y2] = 1

        self.buildSurface(camera)

    #Return a random valid position inside a room
    def getRandomRoomPosition(self, rng):
        i = rng.integers(0, len(self.rooms))
        x = rng.integers(0, self.rooms[i][2])
        y = rng.integers(0, self.rooms[i][3])

        while self.solid[self.rooms[i][0] + x][self.rooms[i][1] + y] == 1:
            i = rng.integers(0, len(self.rooms))
            x = rng.integers(0, self.rooms[i][2])
            y = rng.integers(0, self.rooms[i][3])

        return (self.rooms[i][0] + x, self.rooms[i][1] + y)
    
    def checkValidTile(self, dest):
        return self.solid[dest[0]][dest[1]] == 0

    def draw(self, surf):
        surf.blit(self.surface, (320, 32))