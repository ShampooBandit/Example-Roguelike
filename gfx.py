import pygame
import os

directory = 'gfx/Characters'
f1 = os.path.join(directory, 'Player0.png')
f2 = os.path.join(directory, 'Pest0.png')

directory = 'gfx/Objects'
f3 = os.path.join(directory, 'Floor.png')
f4 = os.path.join(directory, 'Wall.png')

directory = 'gfx/Items'
f5 = os.path.join(directory, 'ShortWep.png')

directory = 'gfx/GUI'
f6 = os.path.join(directory, 'ui_big_pieces.png')

PLAYER_SPRITES = []
MONSTER_SPRITES = []
FLOOR_SPRITES = []
WEAPON_SPRITES = []
GUI_SPRITES = []
GUI_BOX_SPRITES = []

if os.path.isfile(f1):
    PLAYER_SPRITE_SHEET = pygame.image.load_extended(f1)
    PLAYER_SPRITE_SHEET = PLAYER_SPRITE_SHEET.convert_alpha()

    PLAYER_SPRITES.append(PLAYER_SPRITE_SHEET.subsurface(0,0,16,16))

if os.path.isfile(f2):
    MONSTER_SPRITE_SHEET = pygame.image.load_extended(f2)
    MONSTER_SPRITE_SHEET = MONSTER_SPRITE_SHEET.convert_alpha()

    MONSTER_SPRITES.append(MONSTER_SPRITE_SHEET.subsurface(0,0,16,16))

if os.path.isfile(f3):
    FLOOR_SPRITE_SHEET = pygame.image.load_extended(f3)
    FLOOR_SPRITE_SHEET = FLOOR_SPRITE_SHEET.convert_alpha()

    floor_1 = FLOOR_SPRITE_SHEET.subsurface(0,48,112,48)

    FLOOR_SPRITES.append([])
    FLOOR_SPRITES[0].append(floor_1.subsurface(80,0,16,16))  # 0000
    FLOOR_SPRITES[0].append(floor_1.subsurface(48,0,16,16))  # 0001
    FLOOR_SPRITES[0].append(floor_1.subsurface(64,16,16,16)) # 0010
    FLOOR_SPRITES[0].append(floor_1.subsurface(0,0,16,16))   # 0011
    FLOOR_SPRITES[0].append(floor_1.subsurface(96,16,16,16)) # 0100
    FLOOR_SPRITES[0].append(floor_1.subsurface(32,0,16,16))  # 0101
    FLOOR_SPRITES[0].append(floor_1.subsurface(80,16,16,16)) # 0110
    FLOOR_SPRITES[0].append(floor_1.subsurface(16,0,16,16))  # 0111
    FLOOR_SPRITES[0].append(floor_1.subsurface(48,32,16,16)) # 1000
    FLOOR_SPRITES[0].append(floor_1.subsurface(48,16,16,16)) # 1001
    FLOOR_SPRITES[0].append(floor_1.subsurface(0,32,16,16))  # 1010
    FLOOR_SPRITES[0].append(floor_1.subsurface(0,16,16,16))  # 1011
    FLOOR_SPRITES[0].append(floor_1.subsurface(32,32,16,16)) # 1100
    FLOOR_SPRITES[0].append(floor_1.subsurface(32,16,16,16)) # 1101
    FLOOR_SPRITES[0].append(floor_1.subsurface(16,32,16,16)) # 1110
    FLOOR_SPRITES[0].append(floor_1.subsurface(16,16,16,16)) # 1111

if os.path.isfile(f5):
    WEAPON_SPRITE_SHEET = pygame.image.load_extended(f5)
    WEAPON_SPRITE_SHEET = WEAPON_SPRITE_SHEET.convert_alpha()

    WEAPON_SPRITES.append(WEAPON_SPRITE_SHEET.subsurface(0,0,16,16))

if os.path.isfile(f6):
    GUI_SPRITE_SHEET = pygame.image.load_extended(f6)
    GUI_SPRITE_SHEET = GUI_SPRITE_SHEET.convert_alpha()
    #GUI_SPRITE_SHEET.set_colorkey(pygame.Color(255, 255, 255))

    GUI_BOX_SPRITES.append(GUI_SPRITE_SHEET.subsurface(16, 40, 32, 32)) #Top left
    GUI_BOX_SPRITES.append(GUI_SPRITE_SHEET.subsurface(82, 40, 32, 32)) #Top right
    GUI_BOX_SPRITES.append(GUI_SPRITE_SHEET.subsurface(478, 80, 32, 32)) #Bottom left
    GUI_BOX_SPRITES.append(GUI_SPRITE_SHEET.subsurface(544, 80, 32, 32)) #Bottom right
    GUI_BOX_SPRITES.append(GUI_SPRITE_SHEET.subsurface(49, 40, 32, 32)) #Top middle
    GUI_BOX_SPRITES.append(GUI_SPRITE_SHEET.subsurface(478, 24, 32, 32)) #Left middle
    GUI_BOX_SPRITES.append(GUI_SPRITE_SHEET.subsurface(544, 24, 32, 32)) #Right middle
    GUI_BOX_SPRITES.append(GUI_SPRITE_SHEET.subsurface(511, 80, 32, 32)) #Bottom middle

def getTileSprite(index, tiles, center, size):
    x = center[0]
    y = center[1]

    left_x_valid  = (x-1 >= 0)
    right_x_valid = (x+1 < size[0])
    up_y_valid    = (y-1 >= 0)
    down_y_valid  = (y+1 < size[1])

    tile_index_array = ['1' if (up_y_valid    and tiles[x][y-1]==index) else '0',
                        '1' if (left_x_valid  and tiles[x-1][y]==index) else '0',
                        '1' if (right_x_valid and tiles[x+1][y]==index) else '0',
                        '1' if (down_y_valid  and tiles[x][y+1]==index) else '0']
    
    tile_index = int(''.join(tile_index_array), 2)
    
    return FLOOR_SPRITES[index-1][tile_index]