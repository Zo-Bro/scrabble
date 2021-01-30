import sys
import os

import pygame
from pygame.locals import *

import events
import rules

class Global_Vars:
    '''
    All the variables that need to be accessible by any function or class
    '''
    def __init__(self):
        # System Settings
        self._HEIGHT = 720
        self._WIDTH = 1080
        self._FPS = 60

        # Board Dimensions
        self._TILE_SIZE = 32
        self._BORDER_SIZE = 4
        self._BOARD_OFFSET = (50, 100)

        # Font
        self._FONT = 'Cambria'

        # Game Controls
        self._GAME_MODE = 0

        # Colors
        self._ACTIVE_COLOR = (218, 234, 240)
        self._INACTIVE_COLOR = (119, 155, 168)
        self._FONT_COLOR = (35, 80, 97)
        self._HIGHLIGHT_COLOR = (190, 0, 0, 50)
        self._BG_COLOR = ()
        self._TILE_COLOR = ()

    def get_tile_size(self):
        return self._TILE_SIZE
    def set_tile_size(self, val=32):
        self._TILE_SIZE = val

    def get_height(self):
        return self._HEIGHT
    def set_height(self, val=720):
        self._HEIGHT = val

    def get_width(self):
        return self._WIDTH
    def set_width(self, val=1080):
        self._WIDTH = val

    def get_fps(self):
        return self._FPS

    def set_fps(self, val=30):
        if val in [30, 60]:
            self._FPS = val
        else:
            raise AttributeError("The value provided is not a recognized FPS value.")

    def get_game_mode(self):
        return self._GAME_MODE
    def set_game_mode(self, val=0):
        if val in [0, 1, 2, 3]:
            self._GAME_MODE = val
        else:
            raise AttributeError("The number given is not a recognized GAME_MODE value")

    def get_highlight_color(self):
        return self._HIGHLIGHT_COLOR

    def get_border_size(self):
        return self._BORDER_SIZE

    def get_board_offset(self):
        return self._BOARD_OFFSET

    def get_font(self, font_size=12):
        return pygame.font.SysFont( self._FONT, font_size)

    def get_active_color(self):
        return self._ACTIVE_COLOR

    def get_inactive_color(self):
        return self._INACTIVE_COLOR

    def get_font_color(self):
        return self._FONT_COLOR

Globals = Global_Vars()

class Images():
    '''
    A container for all the images of letter tiles and score tiles to be used in sprites.
    '''
    def __init__(self):
        self.images = {}
        for root, dirs, files in os.walk("images"):
            for letter in files:
                letter_name = os.path.splitext(letter)[0]
                image = pygame.image.load(os.path.join(root, letter))
                self.images[letter_name] = image
        '''
        for root, dirs, files in os.walk("images\\numbers"):
            for number in files:
                number_name = os.path.splitext(number)[0]
                image = pygame.image.load(os.path.join("images\\numbers", number))
                print("assigning to number_name: " + number_name)
                self.images[number_name] = image
        for root, dirs files in os.walk()
        '''

IMAGES = Images()

class TextInput:
    '''
    A Text Input Box
    '''
    def __init__(self, position=(0,0), width=200, height=100, font_size=24, max_chars=8):
        self.rect = pygame.Rect(position, (width, height))
        self.color = Globals.get_inactive_color()
        self.font_color = Globals.get_font_color()
        self.font_size = font_size
        self.text = ''
        self.text_surface = Globals.get_font(font_size).render(self.text, True, self.font_color)
        self.active = False
        self.max_chars = max_chars

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_position):
                self.active = True
                self.color = Globals.get_active_color()
            else:
                self.active = False
                self.color = Globals.get_inactive_color()

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.color = Globals.get_inactive_color()
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < self.max_chars:  # max 8 characters
                    self.text += event.unicode

    def update(self, displaySurface):
        pygame.draw.rect(displaySurface, self.color, self.rect)
        self.text_surface = Globals.get_font(self.font_size).render(self.text, True, self.font_color)
        displaySurface.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))

        return
class Button(pygame.sprite.Sprite):
    '''
    A Clickable Button bound to a specific event
    '''
    def __init__(self, text='',
                 position=(Globals.get_height()/2, Globals.get_width()/2),
                 width=20,
                 height=20,
                 font_color=(0,0,0,100),
                 color=(50,50,50,100),
                 color_hover=(70,70,70,100),
                 color_pressed=(30,30,30,100),
                 event = 0):
        super().__init__()
        font = Globals.get_font(35)
        self.color = color
        self.color_hover = color_hover
        self.color_pressed = color_pressed
        self.text = font.render(text, True, font_color)
        self.surf = pygame.surface.Surface((width, height))
        self.surf.fill(color)
        self.rect = self.surf.get_rect(center=position)
        self.event = event
        self.state = 'neutral'
    def update(self, display_surface):
        display_surface.blit(self.surf, self.rect)
        display_surface.blit(self.text, self.rect)

    def hover(self):
        if self.state != 'hover':
            self.state = 'hover'
            self.surf.fill(self.color_hover)
        else:
            pass
    def neutral(self):
        if self.state != 'neutral':
            self.state = 'neutral'
            self.surf.fill(self.color)

    def pressed(self):
        self.surf.fill(self.color_pressed)

    def post_event(self):
        pygame.event.post(self.event)

class ImageSprite(pygame.sprite.Sprite):
    '''
    A simple sprite with an image that can be rendered anywhere
    '''
    def __init__(self, image=None, position=(0,0), set_custom_size = (0,0)):
        super().__init__()
        self.surf = pygame.Surface(image.get_size())
        self.rect = self.surf.get_rect(topleft=position)
        if set_custom_size[0] > 0 and set_custom_size[1] > 0 and image:
            self.custom_size = set_custom_size
            image = pygame.transform.scale(image, self.custom_size)
        else:
            pass
        self.image = image

    def set_image(self, image):
        self.image = pygame.transform.scale(image, self.custom_size)

class Tile(pygame.sprite.Sprite):
    '''
    creates a rectangular sprite for each playable tile.
    the self.coord is only used when the tile is on the game board.

    '''
    def __init__(self, coord=None, image=None, color=(224, 216, 180, 100), position=(0,0)):
        super().__init__()
        self.surf = pygame.Surface((Globals.get_tile_size(),Globals.get_tile_size()))
        self.color = color
        if coord:
            tile_size = Globals.get_tile_size()
            border_size = Globals.get_border_size()
            board_offset = Globals.get_board_offset()
            border_x = tile_size/border_size *coord[0]
            border_y = tile_size/border_size *coord[1]
            self.position = (tile_size * coord[0] + border_x + board_offset[0],
                             tile_size * coord[1]+ border_y + board_offset[1])
            self.rect = self.surf.get_rect(topleft=self.position )
            self.coord = coord
        else:
            self.position = position
            self.rect = self.surf.get_rect(topleft=self.position )

        if type(image) == type(pygame.image):
            self.set_image(image)
        else:
            self.image = None
            self.surf.fill(color)

    def set_image(self, image):
        tile_size = Globals.get_tile_size()

        if image.get_size()[0] > tile_size or image.get_size()[1] > tile_size:
            image = pygame.transform.scale(image, (tile_size, tile_size))
            self.image = image
            self.surf.fill(self.color, special_flags=BLEND_MULT)
            print("image was set!")
        return

class SelectedTile(Tile):
    def __init__(self, coord):
        super().__init__( coord, color=(190, 0, 0, 20))
        self.surf = pygame.Surface((Globals.get_tile_size()+(Globals.get_border_size()*2),
                                    Globals.get_tile_size()+(Globals.get_border_size()*2)))
        self.surf.fill(self.color)
        self.hidden = True
    def move(self, coord):
        if coord != self.coord:
            tile_size = Globals.get_tile_size()
            border_size = Globals.get_border_size()
            board_offset = Globals.get_board_offset()
            self.hidden = False
            border_x = tile_size / border_size * coord[0]
            border_y = tile_size / border_size * coord[1]
            self.rect.update(
                            ((tile_size * coord[0] + border_x + board_offset[0])-(border_size),
                             (tile_size * coord[1]+ border_y + board_offset[1])-(border_size)),
                            (tile_size, tile_size)
                             )
            self.coord = coord
    def hide(self):
        tile_size = Globals.get_tile_size()

        self.rect.update((-tile_size, -tile_size), (tile_size, tile_size))
        self.hidden = True

class Inventory(pygame.sprite.Group):
    '''
    Display  for the tiles in a player's inventory.
    Can re-arrange tiles with mouse.
    Can click and drag tiles
    '''
    def __init__(self, player):
        super().__init__()
        self.bounds_buffer = 20
        tile_size = Globals.get_tile_size()
        border_size = Globals.get_border_size()
        board_offset = Globals.get_board_offset()
        height = Globals.get_height()
        width = Globals.get_width()
        self.bounds = (tile_size+tile_size/4*7, tile_size*2)
        position = (width/2, height - height/10)
        self.player = player
        self.surf= pygame.surface.Surface(self.bounds)
        self.surf.fill((50,50,50,100))
        self.rect = self.surf.get_rect(center=position)
        self.reset_inventory()
        
        self.tile_order = {0:0, 1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7} # display of inventory doesn't change order in back end

    def reset_inventory(self):
        self.empty()
        inventory = self.get_tile_order()
        for tile in inventory:
            
            self.add(Tile(image=IMAGES[tile], position=position))

    def get_inventory(self):
        inventory = self.player.Get_Inventory()
        return inventory

class GameBoard(pygame.sprite.Group):
    '''
    deletes all sprites in this group and regenerates them
    '''
    def __init__(self):
        super().__init__()
        self.bounds_buffer = 20
        self.coords = game_instance.Get_Playboard()
        self.tileImages = Images()
        self.reset_playboard()

    def reset_playboard(self):
        tile_size = Globals.get_tile_size()
        border_size = Globals.get_border_size()
        board_offset = Globals.get_board_offset()
        self.empty()
        for r_index, row in enumerate(self.coords):
            for c_index, column in enumerate(row):
                tileSlot = Tile((c_index, r_index))
                self.add(tileSlot)
        border_x = tile_size / border_size
        border_y = tile_size / border_size

        bounds = ((tile_size + border_x) * len(self.coords) + self.bounds_buffer, # size of board on x axis
                        (tile_size + border_y) * len(self.coords) + self.bounds_buffer) # size on y axis
        self.surf = pygame.surface.Surface(bounds)
        self.surf.fill((50,50,50,100))
        self.rect = self.surf.get_rect(topleft = (board_offset[0]-self.bounds_buffer/2, board_offset[1] -self.bounds_buffer/2)) #position of board

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
            tile.set_image(IMAGES.images[letter])
            return True
        return False

def MainMenu(displaysurface):
    # main menu buttons
    num_players = 2
    name_text = ''
    player_minus_btn = Button(text="Remove Player",
                              position=(200, Globals.get_height()/2),
                              width=200,
                              height=200,
                              event=pygame.event.Event(events.decrease_players_e)
                              )
    player_plus_btn = Button(text="Add Player",
                             position=(600, Globals.get_height()/2),
                             width=200,
                             height=200,
                             event=pygame.event.Event(events.increase_players_e)
                             )
    start_btn = Button(text="Start Game",
                       position=(600, Globals.get_height()-100),
                       width=200,
                       height=200,
                       event=pygame.event.Event(events.game_start_e))
    main_menu_buttons = pygame.sprite.Group(start_btn)
    main_menu_buttons.add([player_minus_btn, player_plus_btn])

    # main menu sprites
    main_menu_bg = ImageSprite(image=IMAGES.images['main_menu_bg'],
                               position=(0,0),
                               set_custom_size=(Globals.get_width(), Globals.get_height())
                               )
    player_count_image = ImageSprite(image=IMAGES.images[str(num_players)],
                                     position=(400, Globals.get_height()/2),
                                     set_custom_size=(200,200)
                                     )
    main_menu_sprites = pygame.sprite.Group([player_count_image])

    # name input box
    box2 = TextInput(position=(100,200))

    in_menu = True
    while in_menu:
        for button in main_menu_buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                button.hover()
            else:
                button.neutral()

        for event in pygame.event.get():
            box2.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                for button in main_menu_buttons:
                    if button.state == 'hover':
                        button.post_event()
            if event.type == events.game_start_e:
                in_menu = False
                return 1
            if event.type == events.increase_players_e:
                print("players increased")
                if num_players < 4:
                    num_players += 1
                    player_count_image.set_image(IMAGES.images[str(num_players)])
            if event.type == events.decrease_players_e:
                if num_players > 2:
                    num_players -= 1
                    player_count_image.set_image(IMAGES.images[str(num_players)])
                print("players decreased")

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # render
            # bg
            displaysurface.blit(main_menu_bg.image, main_menu_bg.rect)
            # buttons
            for button in main_menu_buttons:
                button.update(displaysurface)
            # sprites
            for entity in main_menu_sprites:
                if hasattr(entity, 'image'):
                    displaysurface.blit(entity.image, entity.rect)
                else:
                    displaysurface.blit(entity.surf, entity.rect)
            # input box
            box2.update(displaysurface)

            pygame.display.update()
            FramePerSec.tick(Globals.get_fps())

        # draw buttons
        # handle button events
    return

def Sim(displaysurface, gameboard, game_instance):
    '''
    Loop for simulating the game
    :param displaysurface:
    :return:
    '''
    #=== SIM ===
    # mouse hover over buttons test
    running = True
    selected_tile = SelectedTile((0, 0))
    FOCUS = None
    while running:
        for button in game_buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                button.hover()
            else:
                button.neutral()
        # mouse hover over gameboard test
        if gameboard.rect.collidepoint(pygame.mouse.get_pos()): # only check if within board
            for entity in gameboard:
                is_hover = entity.rect.collidepoint(pygame.mouse.get_pos())
                if is_hover:
                    if entity != FOCUS: #only register a hover event if you hover over a new tile
                        pygame.event.post(pygame.event.Event(events.on_hover_e))
                        FOCUS = entity
        else:
            if not selected_tile.hidden:
                selected_tile.hide()

        # === EVENTS ===
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                for button in game_buttons:
                    if button.state == 'hover':
                        button.post_event()
            if event.type == events.on_hover_e:
                selected_tile.move(FOCUS.coord)
            if event.type == events.place_tile_e:
                # hide tile from player inv
                # update graphic on gameboard
                pass
            if event.type == events.remove_tile_e:
                # show tile in player inv
                # update graphic on gameboard
                pass
            if event.type == events.turn_end_e:
                # give control to next player
                # reload the tiles of the just finished player
                pass
            if event.type == events.lock_in_e:
                # check if word is ok
                # if it is, apply scoring.
                # add a turn_end event to the Q.
                pass
            if event.type == events.game_end_e:
                # show final results screen
                # show end game menu
                pass
            if event.type == events.game_boot_e:
                # show main menu
                pass
            if event.type == events.game_start_e:
                # hide main menu
                # show gameboard
                # begin play sim
                pass
            if event.type == events.test_button_e:
                print("Test button pressed!")
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        #=== RENDER ===
        displaysurface.fill((0,0,0)) # bg (temp)
        # update Game Board Tiles
        displaysurface.blit(gameboard.surf, gameboard.rect) #showing active bounds of board (temp)
        if FOCUS: #Selected tile
            displaysurface.blit(selected_tile.surf, selected_tile.rect)
        for entity in gameboard:
            if entity.image:
                displaysurface.blit(entity.image, entity.rect)
            else:
                displaysurface.blit(entity.surf, entity.rect)
        for button in game_buttons:
            button.update(displaysurface)

        pygame.display.update()
        FramePerSec.tick(Globals.get_fps())
    return



# App Setup
pygame.init()

# setup display
FramePerSec = pygame.time.Clock()
display_surface = pygame.display.set_mode((Globals.get_width(), Globals.get_height()))
pygame.display.set_caption("Scrabble")

#setup pre-sim requirements
game_instance = rules.Scrabble()
game_instance.New_Game()
game_board = GameBoard()
game_board.set_tile_letter((2, 2), 'e')

game_buttons = pygame.sprite.Group()
game_buttons.add(Button("test", event=pygame.event.Event(events.test_button_e)))


all_sprites = pygame.sprite.Group()
all_sprites.add(game_board.sprites())
all_sprites.add(game_buttons.sprites())

# Game Loop

while True:
    if Globals.get_game_mode() == 0:
        print("game mode is 0")
        Globals.set_game_mode(MainMenu(display_surface))
    elif Globals.get_game_mode() == 1:
        print("game mode is 1")
        Globals.set_game_mode(Sim(display_surface, game_board, game_instance))

