import sys
import os

import pygame
from pygame.locals import *

import rules


class TileImages():
    '''
    A container for all the images of letter tiles and score tiles to be used in sprites.
    '''
    def __init__(self):
        self.images = {}
        for root, dirs, files in os.walk("images\\letters"):
            for letter in files:
                letter_name = os.path.splitext(letter)[0]
                self.images[letter_name] = pygame.image.load(os.path.join("images\\letters", letter))

class Tile(pygame.sprite.Sprite):
    '''
    creates a rectangular sprite for each spot on the game board
    fills with a blank color.

    '''
    def __init__(self, coord, image=None, color=(224, 216, 180)):
        super().__init__()
        self.surf = pygame.Surface((TILE_SIZE,TILE_SIZE))
        self.surf.fill(color)
        print("setting rect to " + str(TILE_SIZE * coord[0]) + ',' + str( TILE_SIZE * coord[1]) )
        border_x = TILE_SIZE/4 *coord[0]
        border_y = TILE_SIZE/4 *coord[1]
        self.rect = self.surf.get_rect(topleft=(TILE_SIZE * coord[0] + border_x, TILE_SIZE * coord[1]+ border_y) )
        self.coord = coord
        if type(image) == type(pygame.image):
            self.image = image
        else:
            self.image = None

class GameBoard(pygame.sprite.Group):
    '''
    deletes all sprites in this group and regenerates them
    '''
    def __init__(self):
        super().__init__()
        self.coords = game_instance.Get_Playboard()
        self.tileImages = TileImages()
        self.init_Playboard()

    def init_Playboard(self):
        self.empty()
        for r_index, row in enumerate(self.coords):
            for c_index, column in enumerate(row):
                print("row: {r}, column: {c}".format(r=str(r_index), c=str(c_index)))
                tileSlot = Tile((c_index, r_index))
                self.add(tileSlot)
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

    def set_tile_letter(self, coord = (0,0), letter=None):
        '''
        makes the tile at the given coords render the given letter
        :param coord:
        :param image:
        :return:
        '''
        if letter:
            tile = self.get_tile(coord)
            tile.image = self.tileImages.images[letter]
            tile.surf.blit()
            return True
        return False

pygame.init()
vec = pygame.math.Vector2
TILE_SIZE = 32
# ToDo: create reactive frame size for all monitor resolutions.
# This is possible with the pygame.display
HEIGHT = 1000
WIDTH = 1000
FPS = 60

FramePerSec = pygame.time.Clock()
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scrabble")
game_instance = rules.Scrabble()
game_instance.New_Game()
gameboard = GameBoard()

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    #=== SIM ===

    #=== RENDER ===
    displaysurface.fill((0,0,0)) # bg (temp)
    #update Game Board Graphics
    for entity in gameboard:
        displaysurface.blit(entity.surf, entity.rect)
    pygame.display.update()
    FramePerSec.tick(FPS)

