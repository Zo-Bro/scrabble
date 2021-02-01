import sys
import os

import pygame
from pygame.locals import *
from network import Network

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
        self._HIGHLIGHT_COLOR = (250, 206, 60)
        self._BG_COLOR = ()
        self._TILE_COLOR = (150, 127, 95)
        self._3W_COLOR = (214, 51, 51)
        self._2W_COLOR = (214, 51, 171)
        self._3L_COLOR = (54, 51, 214)
        self._2L_COLOR = (51, 179, 214)
        self._special_color_dict = {
            (3,'w'):self._3W_COLOR,
            (2,'w'):self._2W_COLOR,
            (3,'l'):self._3L_COLOR,
            (2, 'l'):self._2L_COLOR
        }
    def get_special_color(self, code):
        return self._special_color_dict[code]
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

    def get_tile_color(self):
        return self._TILE_COLOR

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

IMAGES = Images()

class TurnTracker:
    #ToDo: Track players by their _ID and not their order in the list.
    '''
    Tracks the names of the players and whose turn it is
    '''
    def __init__(self, name_list = [], position=(0,0), width=200, height=200, font_size=24):
        self.rect=  pygame.Rect(position, (width, height))
        self.color = Globals.get_menu_color()
        self.font_color = Globals.get_font_color()
        self.font_size = font_size
        self.name_surface_list = self.create_text_surfaces(name_list)

    def create_text_surfaces(self, name_list):
        name_surface_list = []
        for name in name_list:
            text_surface = Globals.get_font(self.font_size).render(name + ": 0", True, self.font_color)
            name_surface_list.append(text_surface)
        return name_surface_list

    def next_turn(self, game_instance):
        '''
        updates the score of the names, and also highlights the text of the active persons turn.
        :param game_instance:
        :return:
        '''
        active_player = game_instance.active_player
        new_name_surfaces = []
        for index, name_surface in enumerate(self.name_surface_list):
            if index == active_player:
                font_color = Globals.get_active_color()
            else:
                font_color = self.font_color
            score = game_instance.players[index].get_score()
            name = game_instance.players[index].name
            text = "{}: {}".format(name, score)
            name_surface = Globals.get_font(self.font_size).render(text, True, font_color)
            new_name_surfaces.append(name_surface)
        self.name_surface_list = new_name_surfaces


    def update(self, displaysurface):
        pygame.draw.rect(displaysurface, self.color, self.rect)
        for index, name_surface in enumerate(self.name_surface_list):
            offset = (5, index*50 + 5)
            displaysurface.blit(name_surface, (self.rect.x+offset[0], self.rect.y+offset[1]))
        pass

class TextInput:
    '''
    A Text Input Box
    '''
    def __init__(self, position=(0,0), width=200, height=50, font_size=24, max_chars=8):
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
                 event = events.dummy_e):
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
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hover()
        else:
            self.neutral()

        display_surface.blit(self.surf, self.rect)
        display_surface.blit(self.text, self.rect)

    def hover(self):
        if self.state == 'neutral':
            self.state = 'hover'
            self.surf.fill(self.color_hover)
        else:
            pass

    def neutral(self):
        if self.state != 'neutral':
            self.state = 'neutral'
            self.surf.fill(self.color)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.state == 'hover':
                pygame.event.post(pygame.event.Event(self.event))

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

def invert_coord_y(coord):
    x = coord[0]
    y = coord[1]
    y = 14 - y
    return (x, y)
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
            coord = invert_coord_y(coord)
            tile_size = Globals.get_tile_size()
            border_size = Globals.get_border_size()
            board_offset = Globals.get_board_offset()
            border_x = tile_size/border_size *coord[0]
            border_y = tile_size/border_size *coord[1]
            self.position = (tile_size * coord[0] + border_x + board_offset[0],
                             tile_size * coord[1]+ border_y + board_offset[1]) # y
            self.rect = self.surf.get_rect(topleft=self.position )
            self.coord = coord
        else:
            self.position = position
            self.rect = self.surf.get_rect(topleft=self.position )

        if image is not None:
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
        return

class SelectedTile(Tile):
    def __init__(self, coord):
        super().__init__( coord, color=Globals.get_highlight_color())
        self.surf = pygame.Surface((Globals.get_tile_size()+(Globals.get_border_size()*2),
                                    Globals.get_tile_size()+(Globals.get_border_size()*2)))
        self.surf.fill(self.color)
        self.hidden = True
    def move(self, coord=None, position=None):
        if position:
            tile_size = Globals.get_tile_size()
            border_size = Globals.get_border_size()
            board_offset = Globals.get_board_offset()
            self.hidden = False
            self.rect.update(position, (tile_size, tile_size))
            return
        else:
            if coord != self.coord:
                tile_size = Globals.get_tile_size()
                border_size = Globals.get_border_size()
                board_offset = Globals.get_board_offset()
                self.hidden = False
                border_x = tile_size / border_size * coord[0]
                border_y = tile_size / border_size * coord[1]
                self.rect.update(
                                ((tile_size * coord[0] + border_x + board_offset[0])-(border_size), # x position
                                 (tile_size * coord[1]+ border_y + board_offset[1])-(border_size)), # y position
                                (tile_size, tile_size) # width, height
                                 )
                self.coord = coord
    def hide(self):
        tile_size = Globals.get_tile_size()

        self.rect.update((-tile_size, -tile_size), (tile_size, tile_size)) #hides just off screen
        self.hidden = True


class Inventory(pygame.sprite.Group):
    '''
    Display  for the tiles in a player's inventory.
    Can re-arrange tiles with mouse.
    Can click and drag tiles
    '''
    def __init__(self, letters=[]):
        super().__init__()
        self.bounds_buffer = 20
        tile_size = Globals.get_tile_size()
        border_size = Globals.get_border_size()
        board_offset = Globals.get_board_offset()
        height = Globals.get_height()
        width = 700
        self.bounds = (7*(tile_size + border_size), tile_size+(border_size)) # x = 7 tiles wide with some buffer, y = 2 tiles tall
        self.position = (width, (height - height/10)) # x = center, y = close to edge
        self.surf= pygame.surface.Surface(self.bounds)
        self.surf.fill((50,50,50,100))
        self.rect = self.surf.get_rect(topleft=self.position)
        self.reset_inventory(letters)
        

    def reset_inventory(self, letters):
        self.empty()
        for index, letter in enumerate(letters):
            position = (self.position[0]+ index*(Globals.get_tile_size() + Globals.get_border_size()), self.position[1])
            self.add(Tile(image=IMAGES.images[letter], position=position))

    def get_inventory(self):
        inventory = self.player.Get_Inventory()
        return inventory

    def update(self, displaysurface):
        for tile in self.sprites():
            displaysurface.blit(tile.image, tile.rect)

class GameBoard(pygame.sprite.Group):
    '''
    Contains All Tile Sprites on the Board
    '''
    def __init__(self, game_instance):
        super().__init__()
        self.bounds_buffer = 20
        self.coords = game_instance.Get_Playboard()
        self.tileImages = Images()
        self.reset_playboard(game_instance.special_tiles)

    def reset_playboard(self, special_tiles):
        tile_size = Globals.get_tile_size()
        border_size = Globals.get_border_size()
        board_offset = Globals.get_board_offset()
        self.empty()
        for r_index, row in enumerate(self.coords):
            for c_index, column in enumerate(row):
                coord_code = (c_index,r_index)
                if coord_code in special_tiles.keys():
                    tile_color = Globals.get_special_color(special_tiles[coord_code])
                else:
                    tile_color = Globals.get_tile_color()
                tileSlot = Tile((c_index, r_index), color=tile_color)
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
            if sprite.coord == invert_coord_y(coord):
                return sprite
        return None

    def set_tile(self, letter='', coord = (0, 0)):
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

def MainMenu(displaysurface, game_instance):
    # main menu buttons
    num_players = 2
    name_text = ''
    player_minus_btn = Button(text="Remove Player",
                              position=(200, Globals.get_height()/2),
                              width=150,
                              height=50,
                              event=events.decrease_players_e
                              )
    player_plus_btn = Button(text="Add Player",
                             position=(600, Globals.get_height()/2),
                             width=150,
                             height=50,
                             event=events.increase_players_e
                             )
    start_btn = Button(text="Start Game",
                       position=(600, Globals.get_height()-100),
                       width=150,
                       height=50,
                       event=events.game_start_e)
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
    name_input = TextInput(position=(100,200))

    in_menu = True
    while in_menu:
        for button in main_menu_buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                button.hover()
            else:
                button.neutral()

        for event in pygame.event.get():
            name_input.handle_event(event)
            for button in main_menu_buttons:
                button.handle_event(event)
            if event.type == events.game_start_e:
                in_menu = False
                game_instance.Generate_Players(num_players)
                game_instance.players[0].name = name_text
                return 1
            if event.type == events.increase_players_e:
                print("players increased")
                if num_players < 4:
                    num_players += 1
                    player_count_image.set_image(IMAGES.images[str(num_players)])
                    game_instance.num_players = num_players

            if event.type == events.decrease_players_e:
                if num_players > 2:
                    num_players -= 1
                    player_count_image.set_image(IMAGES.images[str(num_players)])
                    game_instance.num_players = num_players

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
            name_input.update(displaysurface)

            pygame.display.update()
            FramePerSec.tick(Globals.get_fps())

        # draw buttons
        # handle button events
    return

def Sim(displaysurface, gameboard, game_model):
    '''
    Loop for simulating the game
    :param displaysurface:
    :return:
    '''
    #=== SIM ===
    # mouse hover over buttons test
    running = True
    selected_tile = SelectedTile((0, 0))
    selected_inv_tile = SelectedTile((0,0))
    focus = None
    focus_inv = None
    p1 = game_model.players[0]

    player_inv = Inventory(p1.Get_Inventory())

    # TEMP, detecting words test
    detect_word_btn = Button("detect word", (800, 500), 100, 100, event=events.test_detect_word_e)
    apple_played = 'apple'
    coords = (7,7)
    apple_coords = []
    for index, letter in enumerate(apple_played):
        game_model.Set_Letter(letter, (7 + index, 7))
        gameboard.set_tile(letter, (7 + index, 7))
        apple_coords.append((7+index, 7))
    letters_played = 'ae'
    latest_coords = [(8,8), (8,6)]
    for letter, coord in zip(letters_played, latest_coords):
        game_model.Set_Letter(letter, coord)
        gameboard.set_tile(letter, coord)


    while running:
        if game_model.p1_went == True:
            player_inv.reset_inventory(p1.Get_Inventory())
            game_model.p1_went = False
        # mouse hover over gameboard test
        if gameboard.rect.collidepoint(pygame.mouse.get_pos()): # only check if within board
            for entity in gameboard:
                is_hover = entity.rect.collidepoint(pygame.mouse.get_pos())
                if is_hover:
                    if entity != focus: #only register a hover event if you hover over a new tile
                        pygame.event.post(pygame.event.Event(events.on_hover_e))
                        focus = entity
        else:
            if not selected_tile.hidden:
                selected_tile.hide()
        if player_inv.rect.collidepoint(pygame.mouse.get_pos()):
            for entity in player_inv:
                is_inv_hover = entity.rect.collidepoint(pygame.mouse.get_pos())
                if is_inv_hover:
                    if entity != focus_inv:
                        pygame.event.post(pygame.event.Event(events.on_hover_inv_e))
                        focus_inv = entity
                        print("selected new entity!")
        else:
            if not selected_inv_tile.hidden:
                selected_inv_tile.hide()

        # === EVENTS ===
        for event in pygame.event.get():
            detect_word_btn.handle_event(event)
            if event.type == events.test_detect_word_e:
                all_unique_words_made = []

                # for each letter played, find any words that it constructs
                for letter, coord in zip(apple_played, apple_coords):
                    full_words, full_words_coords = game_model.Detect_words(letter, coord)

                    # only keep a successfully constructed word the first time.
                    for word, coords in zip(full_words, full_words_coords):
                        if [word, coords] not in all_unique_words_made:
                            all_unique_words_made.append([word, coords])
                score = 0
                is_valid = False
                for word_coords in all_unique_words_made:
                    is_valid = game_model.Check_Word_Validity(word_coords[0])
                    if is_valid:
                        score += game_model.Calculate_Score(word_coords[0], word_coords[1])
                    else:
                        #ToDo: keep a copy of the game_model's state before the play was made. If the play is invalid, revert to that state
                        print("INVALID PLAY! ")
                if is_valid:
                    print("The play was successful! the score earned is: " + str(score))
                    print("The words that achieved that score are:")
                    for word_coords in all_unique_words_made:
                        print(word_coords[0])






            if event.type == events.on_hover_e:
                selected_tile.move(coord=focus.coord)
            if event.type == events.on_hover_inv_e:
                selected_inv_tile.move(position=focus_inv.position)
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
        displaysurface.blit(player_inv.surf, player_inv.rect)
        if focus: #Selected tile
            displaysurface.blit(selected_tile.surf, selected_tile.rect)
        if focus_inv:
            displaysurface.blit(selected_inv_tile.surf, selected_inv_tile.rect)
        for entity in gameboard:
            if entity.image:
                displaysurface.blit(entity.image, entity.rect)
            else:
                displaysurface.blit(entity.surf, entity.rect)
        detect_word_btn.update(displaysurface)
        player_inv.update(displaysurface)
        pygame.display.update()
        FramePerSec.tick(Globals.get_fps())
    return


def Main():
    display_surface = pygame.display.set_mode((Globals.get_width(), Globals.get_height()))
    pygame.display.set_caption("Scrabble")

    #setup pre-sim requirements
    #ToDo: Make a Lobby that lets you wait for players to join.
    game_model = rules.Scrabble()
    game_model.New_Game()
    game_board = GameBoard(game_model)


    
    game_buttons = pygame.sprite.Group()
    game_buttons.add(Button("test", event=pygame.event.Event(events.test_button_e)))


    all_sprites = pygame.sprite.Group()
    all_sprites.add(game_board.sprites())
    all_sprites.add(game_buttons.sprites())

    # Game Loop
    while True:
        if Globals.get_game_mode() == 0:
            print("game mode is 0")
            Globals.set_game_mode(MainMenu(display_surface, game_model))
        elif Globals.get_game_mode() == 1:
            print("game mode is 1")
            Globals.set_game_mode(Sim(display_surface, game_board, game_model))


if __name__ == '__main__':
    # App Setup
    pygame.init()

    # setup display
    FramePerSec = pygame.time.Clock()

    Main()