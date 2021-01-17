import sys
import os

import pygame
from pygame.locals import *

import rules

HIGHLIGHT_COLOR = (190, 0, 0, 100)
BORDER_SIZE = 4
BOARD_OFFSET = (50, 100)

class Inventory():
    '''
    Display  for the tiles in a player's inventory.
    Can re-arrange tiles with mouse.
    Can click and crag tiles
    '''
    def __init__(self, tiles=[]):
        self.tiles = tiles
    def draw(self):
        for tile in self.tiles:
            pass
        pass


class TileImages():
    '''
    A container for all the images of letter tiles and score tiles to be used in sprites.
    '''
    def __init__(self):
        self.images = {}
        for root, dirs, files in os.walk("images\\letters"):
            for letter in files:
                letter_name = os.path.splitext(letter)[0]
                image = pygame.image.load(os.path.join("images\\letters", letter))
                self.images[letter_name] = image

class Tile(pygame.sprite.Sprite):
    '''
    creates a rectangular sprite for each playable tile.
    the self.coord is only used when the tile is on the game board.

    '''
    def __init__(self, coord, image=None, color=(224, 216, 180, 100)):
        super().__init__()
        self.surf = pygame.Surface((TILE_SIZE,TILE_SIZE))
        self.color = color
        border_x = TILE_SIZE/BORDER_SIZE *coord[0]
        border_y = TILE_SIZE/BORDER_SIZE *coord[1]
        position = (TILE_SIZE * coord[0] + border_x + BOARD_OFFSET[0], TILE_SIZE * coord[1]+ border_y + BOARD_OFFSET[1])
        self.rect = self.surf.get_rect(topleft=position )
        self.coord = coord
        if type(image) == type(pygame.image):
            self.set_image(image)
        else:
            self.image = None
            self.surf.fill(color)

    def set_image(self, image):
        if image.get_size()[0] > TILE_SIZE or image.get_size()[1] > TILE_SIZE:
            image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
            self.image = image
            self.surf.fill(self.color, special_flags=BLEND_MULT)
            print("image was set!")
        return

class SelectedTile(Tile):
    def __init__(self, coord):
        super().__init__( coord, color=(190, 0, 0, 20))
        self.hidden = True
    def move(self, coord):
        if coord != self.coord:
            self.hidden = False
            border_x = TILE_SIZE / BORDER_SIZE * coord[0]
            border_y = TILE_SIZE / BORDER_SIZE * coord[1]
            self.rect.update((TILE_SIZE * coord[0] + border_x + BOARD_OFFSET[0], TILE_SIZE * coord[1]+ border_y + BOARD_OFFSET[1]), (TILE_SIZE, TILE_SIZE))
            self.coord = coord
    def hide(self):
        self.rect.update((-TILE_SIZE, -TILE_SIZE), (TILE_SIZE, TILE_SIZE))
        self.hidden = True


class GameBoard(pygame.sprite.Group):
    '''
    deletes all sprites in this group and regenerates them
    '''
    def __init__(self):
        super().__init__()
        self.bounds_buffer = 20
        self.coords = game_instance.Get_Playboard()
        self.tileImages = TileImages()
        self.init_Playboard()

    def init_Playboard(self):
        self.empty()
        for r_index, row in enumerate(self.coords):
            for c_index, column in enumerate(row):
                tileSlot = Tile((c_index, r_index))
                self.add(tileSlot)
        border_x = TILE_SIZE / BORDER_SIZE
        border_y = TILE_SIZE / BORDER_SIZE

        board_bounds = ((TILE_SIZE + border_x) * len(self.coords) + self.bounds_buffer, # x
                        (TILE_SIZE + border_y) * len(self.coords) + self.bounds_buffer) # y
        self.surf = pygame.surface.Surface(board_bounds)
        self.surf.fill((50,50,50,100))
        self.rect = self.surf.get_rect(topleft = (BOARD_OFFSET[0]-self.bounds_buffer/2, BOARD_OFFSET[1] -self.bounds_buffer/2))

        return

    def get_tile(self, coord= (0,0)):
        '''
        return the sprite at the given coords
        :param coord:
        :return:
        '''
        for sprite in self.sprites():
            if sprite.coord == coord:
                return sprite
        return None

    def set_tile_letter(self, coord = (0,0), letter=''):
        '''
        makes the tile at the given coords render the given letter
        :param coord:
        :param image:
        :return:
        '''
        if letter:
            tile = self.get_tile(coord)
            tile.set_image(self.tileImages.images[letter])
            return True
        return False

pygame.init()
TILE_SIZE = 32
# ToDo: create reactive frame size for all monitor resolutions.
# This is possible with the pygame.display
HEIGHT = 1000
WIDTH = 1000
FPS = 60

# setup display
FramePerSec = pygame.time.Clock()
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scrabble")

# Create Global Events
turn_end_e = pygame.USEREVENT + 1
lock_in_e = pygame.USEREVENT + 2 #apply your letters to the board
on_hover_e = pygame.USEREVENT + 3 # if mouse on Tile() class sprite
place_tile_e  = pygame.USEREVENT + 4
remove_tile_e  = pygame.USEREVENT + 5
game_end_e  = pygame.USEREVENT + 6
game_boot_e  = pygame.USEREVENT + 7
game_start_e  = pygame.USEREVENT + 8

#setup pre-sim requirements
game_instance = rules.Scrabble()
game_instance.New_Game()
gameboard = GameBoard()
gameboard.set_tile_letter((2, 2), 'e')
FOCUS = None
selected_tile = SelectedTile((0,0))

# Game Loop
while True:

    #=== SIM ===
    # mouse hover test
    if gameboard.rect.collidepoint(pygame.mouse.get_pos()): # only check if within board
        for entity in gameboard:
            is_hover = entity.rect.collidepoint(pygame.mouse.get_pos())
            if is_hover:
                if entity != FOCUS: #only register a hover event if you hover over a new tile
                    pygame.event.post(pygame.event.Event(on_hover_e))
                    FOCUS = entity
    else:
        if not selected_tile.hidden:
            selected_tile.hide()

    # === EVENTS ===
    for event in pygame.event.get():
        if event.type == on_hover_e:
            selected_tile.move(FOCUS.coord)
        if event.type == place_tile_e:
            # hide tile from player inv
            # update graphic on gameboard
            pass
        if event.type == remove_tile_e:
            # show tile in player inv
            # update graphic on gameboard
            pass
        if event.type == turn_end_e:
            # give control to next player
            # reload the tiles of the just finished player
            pass
        if event.type == lock_in_e:
            # check if word is ok
            # if it is, apply scoring.
            # add a turn_end event to the Q.
            pass
        if event.type == game_end_e:
            # show final results screen
            # show end game menu
            pass
        if event.type == game_boot_e:
            # show main menu
            pass
        if event.type == game_start_e:
            # hide main menu
            # show gameboard
            # begin play sim
            pass
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    #=== RENDER ===
    displaysurface.fill((0,0,0)) # bg (temp)

    # update Game Board Tiles
    displaysurface.blit(gameboard.surf, gameboard.rect) #showing active bounds of board (temp)
    for entity in gameboard:
        if entity.image:
            displaysurface.blit(entity.image, entity.rect)
        else:
            displaysurface.blit(entity.surf, entity.rect)
    if FOCUS: #Selected tile
        displaysurface.blit(selected_tile.surf, selected_tile.rect)

    pygame.display.update()
    FramePerSec.tick(FPS)

