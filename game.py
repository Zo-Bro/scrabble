import sys
import os
from _thread import *

import pygame
from pygame.locals import *

from network import Network
from server import Server
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
        self._SELECTED_TILE_COLOR = (158, 235, 52)
        self._ACTIVE_COLOR = (218, 234, 240)
        self._INACTIVE_COLOR = (119, 155, 168)
        self._REQUIRED_TILE_COLOR = (50, 155, 168)
        self._FONT_COLOR = (35, 80, 97)
        self._HIGHLIGHT_COLOR = (250, 206, 60)
        self._BG_COLOR = ()
        self._TILE_COLOR = (150, 127, 95)
        self._3W_COLOR = (214, 51, 51)
        self._2W_COLOR = (214, 51, 171)
        self._3L_COLOR = (54, 51, 214)
        self._2L_COLOR = (51, 179, 214)
        self._special_color_dict = {
            (3, 'w'): self._3W_COLOR,
            (2, 'w'): self._2W_COLOR,
            (3, 'l'): self._3L_COLOR,
            (2, 'l'): self._2L_COLOR
        }

    def get_required_tile_color(self):
        return self._REQUIRED_TILE_COLOR

    def get_selected_tile_color(self):
        return self._SELECTED_TILE_COLOR

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
        return pygame.font.SysFont(self._FONT, font_size)

    def get_active_color(self):
        return self._ACTIVE_COLOR

    def get_inactive_color(self):
        return self._INACTIVE_COLOR

    def get_font_color(self):
        return self._FONT_COLOR

    def get_tile_color(self):
        return self._TILE_COLOR


Globals = Global_Vars()


class Images:
    """
    A container for all the images of letter tiles and score tiles to be used in sprites.
    Also allows reverse lookup by the image for letters, specifically
    mirrors the images folder in structure
    """

    def __init__(self):
        self.letters = {}
        self.letter_img = {}
        self.numbers = {}
        self.bgs = {}
        self.buttons = {}
        for root, dirs, files in os.walk(r"images\letters"):
            for letter in files:
                letter_name = os.path.splitext(letter)[0]
                letter_name = letter_name.rsplit('_')[0]
                image = pygame.image.load(os.path.join(root, letter))
                self.letters[letter_name] = image
                self.letter_img[image] = letter_name

        for root, dirs, files in os.walk(r"images\numbers"):
            for number in files:
                num_name = os.path.splitext(number)[0]
                num_name = num_name.rsplit('_')[0]
                num_name = num_name.lstrip('0')
                image = pygame.image.load(os.path.join(root, number))
                self.letters[num_name] = image
                self.letter_img[image] = num_name
        for root, dirs, files in os.walk(r"images\bgs"):
            for item in files:
                item_name = os.path.splitext(item)[0]
                item_name = item_name.rsplit('_')[0]
                image = pygame.image.load(os.path.join(root, item))
                self.bgs[item_name] = image


IMAGES = Images()


class TurnTracker:
    # ToDo: Track players by their _ID and not their order in the list.
    """
    Tracks the names of the players and whose turn it is
    """

    def __init__(self, name_list=[], position=(0, 0), width=200, height=200, font_size=24):
        self.rect = pygame.Rect(position, (width, height))
        self.color = Globals.get_menu_color()
        self.font_color = Globals.get_font_color()
        self.font_size = font_size
        self.name_surface_list = self.create_text_surfaces(name_list)

    def add_player(self, name, id):
        return

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
            offset = (5, index * 50 + 5)
            displaysurface.blit(name_surface, (self.rect.x + offset[0], self.rect.y + offset[1]))
        pass


class NamePlate(pygame.sprite.Sprite):
    '''
    An Image displaying a players name
    '''

    def __init__(self):
        self.width = 200
        self.height = 50
        self.rect = pygame.Rect((0, 0), (self.width, self.height))
        self.color = Globals.get_inactive_color()
        self.font_color = (255, 255, 255)
        self.font_size = 36
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill(self.color)

    def set_name(self, name):
        self.name = name
        self.text = name
        self.text_surface = Globals.get_font(self.font_size).render(self.text, True, self.font_color)

    def update(self, displaysurface, position, active=False, me=False, score=0):
        if score:
            self.text = self.name + ": " + str(score)
            self.text_surface = Globals.get_font(self.font_size).render(self.text, True, self.font_color)
        self.rect.update(position, (self.width, self.height))
        displaysurface.blit(self.surf, self.rect)
        displaysurface.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))
        if active:
            if me:
                self.surf.fill(Globals.get_active_color())
            else:
                self.surf.fill(self.color)
            displaysurface.blit(pygame.Surface((20, 20)), (
            self.rect.x - self.width / 2, self.rect.y))  # draw a square next the active player (temp)



class TextInput:
    '''
    A Text Input Box
    '''

    def __init__(self, position=(0, 0), width=200, height=50, font_size=24, max_chars=8, default_text=''):
        self.rect = pygame.Rect(position, (width, height))
        self.color = Globals.get_inactive_color()
        self.font_color = Globals.get_font_color()
        self.font_size = font_size
        self.text = default_text
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
        displaySurface.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))

        return

class PopUp:
    """
    a window that holds other widgets.
    """
    def __init__(self, position=(100,100), width=300, height=200):
        self.position = position
        self.width = width
        self.height = height
        self.surf = pygame.Surface((self.width, self.height), position)
        self.rect = pygame.Rect(self.position, (self.width, self.height))
        #self.close_event = pygame.event.

    def handle_event(self):
        pass

class TextBox():
    """
    An easy way to render text to the screen
    """
    def __init__(self, text='',
                 position=(100, 100),
                 width=300,
                 height=200,
                 font_color=(0, 0, 0),
                 color=(50, 50, 50),
                 bg_image=None,
                 button='ok'):
        self.text = text
        self.position = position
        self.width = width
        self.height = height
        self.font_color = font_color
        self.color = color
        self.surf = pygame.Surface((self.width, self.height), position)

        if bg_image:
            self.set_image(bg_image)

    def set_image(self, image):
        size = (self.width, self.height)
        if image.get_size()[0] > self.width or image.get_size()[1] > self.height:
            image = pygame.transform.scale(image, size)
            self.image = image
            self.surf.fill(self.color)
        return


class Button(pygame.sprite.Sprite):
    """
    A Clickable Button bound to a specific event
    """

    def __init__(self, text='',
                 position=(Globals.get_height() / 2, Globals.get_width() / 2),
                 width=20,
                 height=20,
                 font_color=(0, 0, 0, 100),
                 color=(50, 50, 50, 100),
                 color_hover=(70, 70, 70, 100),
                 color_pressed=(30, 30, 30, 100),
                 event=events.dummy_e):
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
        self._hidden = False

    def hide(self, hide_bool=True):
        self._hidden = hide_bool

    def update(self, display_surface, active=True):
        if not self._hidden:
            if not active:
                self.inactive()
            elif self.rect.collidepoint(pygame.mouse.get_pos()):
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

    def inactive(self):
        if self.state != 'inactive':
            self.state = 'inactive'
            self.surf.fill(Globals.get_inactive_color())

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.state == 'hover':
                pygame.event.post(pygame.event.Event(self.event))


class ImageSprite(pygame.sprite.Sprite):
    """
    A simple sprite with an image that can be rendered anywhere
    """

    def __init__(self, image=None, position=(0, 0), set_custom_size=(0, 0)):
        super().__init__()
        if set_custom_size[0] > 0 and set_custom_size[1] > 0 and image:
            self.custom_size = set_custom_size
            image = pygame.transform.scale(image, self.custom_size)
        else:
            self.custom_size = image.get_size()
        self.surf = pygame.Surface(image.get_size())
        self.rect = self.surf.get_rect(center=position)
        self.image = image

    def set_image(self, image):
        self.image = pygame.transform.scale(image, self.custom_size)


def invert_coord_y(coord):
    x = coord[0]
    y = coord[1]
    y = 14 - y
    return x, y


class Tile(pygame.sprite.Sprite):
    """
    creates a rectangular sprite for each playable tile.
    the self.coord is only used when the tile is on the game board.

    """

    def __init__(self, coord=None, image=None, color=(224, 216, 180, 100), position=(0, 0)):
        super().__init__()
        tile_size = Globals.get_tile_size()
        border_size = Globals.get_border_size()
        board_offset = Globals.get_board_offset()
        self.surf = pygame.Surface((Globals.get_tile_size(), Globals.get_tile_size()))
        self.color = color
        if coord:
            coord = invert_coord_y(coord)
            border_x = tile_size / border_size * coord[0]
            border_y = tile_size / border_size * coord[1]
            self.position = (tile_size * coord[0] + border_x + board_offset[0],
                             tile_size * coord[1] + border_y + board_offset[1])  # y
            self.rect = self.surf.get_rect(topleft=self.position)
            self.coord = coord
        else:
            self.position = position
            self.rect = self.surf.get_rect(topleft=self.position)
        self.selected_surf = pygame.Surface((tile_size + border_size * 2, tile_size + border_size * 2))
        self.selected_surf.fill(Globals.get_selected_tile_color())
        self.selected_surf.set_alpha(128)
        self.selected_rect = self.selected_surf.get_rect(
            topleft=(self.position[0] - border_size, self.position[1] - border_size))
        self.required_surf = pygame.Surface((tile_size + border_size * 2, tile_size + border_size * 2))
        self.required_surf.fill(Globals.get_required_tile_color())
        self.required_rect = self.selected_surf.get_rect(
            topleft=(self.position[0] - border_size, self.position[1] - border_size))
        if image is not None:
            self.set_image(image)
        else:
            self.image = None
            self.surf.fill(color)

    def set_image(self, image):
        tile_size = Globals.get_tile_size()
        self.letter = IMAGES.letter_img[image]
        if image.get_size()[0] > tile_size or image.get_size()[1] > tile_size:
            image = pygame.transform.scale(image, (tile_size, tile_size))
            self.image = image
            self.surf.fill(self.color)
        return

    def handle_event(self, event):
        '''
        if you click this tile, set a highlight around it and then return itself
        :param event:
        :return:
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    return True, self
        return False, None

    def reset(self):
        self.image = None


class SelectedTile(Tile):
    def __init__(self, coord):
        super().__init__(coord, color=Globals.get_highlight_color())
        self.surf = pygame.Surface((Globals.get_tile_size() + (Globals.get_border_size() * 2),
                                    Globals.get_tile_size() + (Globals.get_border_size() * 2)))
        self.surf.fill(self.color)
        self.surf.set_alpha(128)
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
                    ((tile_size * coord[0] + border_x + board_offset[0]) - (border_size),  # x position
                     (tile_size * coord[1] + border_y + board_offset[1]) - (border_size)),  # y position
                    (tile_size, tile_size)  # width, height
                )
                self.coord = coord

    def hide(self):
        tile_size = Globals.get_tile_size()

        self.rect.update((-tile_size, -tile_size), (tile_size, tile_size))  # hides just off screen
        self.hidden = True


class Inventory(pygame.sprite.Group):
    '''
    Display  for the tiles in a player's inventory.
    '''

    def __init__(self, letters=[]):
        super().__init__()
        self.bounds_buffer = 20
        tile_size = Globals.get_tile_size()
        border_size = Globals.get_border_size()
        board_offset = Globals.get_board_offset()
        height = Globals.get_height()
        width = 700
        self.bounds = (
        7 * (tile_size + border_size), tile_size + (border_size))  # x = 7 tiles wide with some buffer, y = 2 tiles tall
        self.position = (width, (height - height / 10))  # x = center, y = close to edge
        self.surf = pygame.surface.Surface(self.bounds)
        self.surf.fill((50, 50, 50, 100))
        self.rect = self.surf.get_rect(topleft=self.position)
        self.reset_inventory(letters)

    def reset_inventory(self, letters):
        self.empty()
        for index, letter in enumerate(letters):
            position = (
            self.position[0] + index * (Globals.get_tile_size() + Globals.get_border_size()), self.position[1])
            self.add(Tile(image=IMAGES.letters[letter], position=position))

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
        '''
        deletes all sprites and regenerates
        :param special_tiles:
        :return:
        '''
        tile_size = Globals.get_tile_size()
        border_size = Globals.get_border_size()
        board_offset = Globals.get_board_offset()
        self.empty()
        for r_index, row in enumerate(self.coords):
            for c_index, column in enumerate(row):
                coord_code = (c_index, r_index)
                if coord_code in special_tiles.keys():
                    tile_color = Globals.get_special_color(special_tiles[coord_code])
                else:
                    tile_color = Globals.get_tile_color()
                tileSlot = Tile((c_index, r_index), color=tile_color)
                self.add(tileSlot)
        border_x = tile_size / border_size
        border_y = tile_size / border_size

        bounds = ((tile_size + border_x) * len(self.coords) + self.bounds_buffer,  # size of board on x axis
                  (tile_size + border_y) * len(self.coords) + self.bounds_buffer)  # size on y axis
        self.surf = pygame.surface.Surface(bounds)
        self.surf.fill((50, 50, 50, 100))
        self.rect = self.surf.get_rect(topleft=(
        board_offset[0] - self.bounds_buffer / 2, board_offset[1] - self.bounds_buffer / 2))  # position of board

        return

    def get_tile(self, coord=(0, 0)):
        '''
        return the sprite at the given coords
        :param coord:
        :return:
        '''
        for sprite in self.sprites():
            if sprite.coord == coord:
                return sprite
        return None

    def set_tile(self, letter='', coord=(0, 0)):
        '''
        makes the tile at the given coords render the given letter
        :param coord:
        :param image:
        :return:
        '''
        tile = self.get_tile(coord)

        if letter:
            tile.set_image(IMAGES.letters[letter])
            return True
        else:
            tile.reset()
        return False

    def update_from_model(self, game_model):
        playboard = game_model.Get_Playboard()
        for y, column in enumerate(playboard):
            for x, value in enumerate(column):
                self.set_tile(value, (x, y))


"""
def ParticleSystem():

    def __init__(self):
        '''
        Container for particle effects. Each function can be an effect that plays at a given position.
        :param self:
        :return:
        '''
        self.active_effects = []
        self.fx_library = {
            'sparkle':
        }
        pass

    def q_sparkle(self, position):
        # queue up a sparkle effect.
        self.active_effects.append(['sparkle', 60, position])
        return

    def update(self, displaysurface):
        for effect in self.active_effects:
            name = effect[0]
            timer = effect[1]
"""


class Game:
    def __init__(self):
        self.server = None
        self.network = None

    def MainMenu(self, displaysurface):
        # main menu buttons
        num_players = 2
        name_text = ''
        player_minus_btn = Button(text="- Player",
                                  position=(200, Globals.get_height() / 2),
                                  width=150,
                                  height=50,
                                  event=events.decrease_players_e
                                  )
        player_plus_btn = Button(text="+ Player",
                                 position=(600, Globals.get_height() / 2),
                                 width=150,
                                 height=50,
                                 event=events.increase_players_e
                                 )
        server_btn = Button(text="Host Server",
                            position=(600, Globals.get_height() - 100),
                            width=150,
                            height=50,
                            event=events.server_start_e)

        join_btn = Button(text="Join Game",
                          position=(800, Globals.get_height() - 100),
                          width=150,
                          height=50,
                          event=events.connect_to_server_e
                          )

        main_menu_buttons = pygame.sprite.Group([server_btn, join_btn])

        main_menu_buttons.add([player_minus_btn, player_plus_btn])

        # text input
        name_input = TextInput(position=(100, 200), default_text='<enter name>')
        server_IP_input = TextInput(position=(800, Globals.get_height() - 200),
                                    width=200,
                                    height=100,
                                    font_size=36,
                                    max_chars=36,
                                    default_text='192.168.1.2'
                                    )
        # main menu sprites
        main_menu_bg = ImageSprite(image=IMAGES.bgs['blue'],
                                   position=(Globals.get_width() / 2, Globals.get_height() / 2),
                                   set_custom_size=(Globals.get_width(), Globals.get_height())
                                   )
        player_count_image = ImageSprite(image=IMAGES.letters[str(num_players)],
                                         position=(400, Globals.get_height() / 2),
                                         set_custom_size=(100, 100)
                                         )
        main_menu_sprites = pygame.sprite.Group([player_count_image])

        # pop up windows

        pop_up_grp = pygame.sprite.Group()

        in_menu = True
        while in_menu:
            for button in main_menu_buttons:
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    button.hover()
                else:
                    button.neutral()

            for event in pygame.event.get():
                name_input.handle_event(event)
                server_IP_input.handle_event(event)

                for button in main_menu_buttons:
                    button.handle_event(event)

                if event.type == events.increase_players_e:
                    print("players increased")
                    if num_players < 4:
                        num_players += 1
                        player_count_image.set_image(IMAGES.letters[str(num_players)])

                if event.type == events.decrease_players_e:
                    if num_players > 2:
                        num_players -= 1
                        player_count_image.set_image(IMAGES.letters[str(num_players)])

                    print("players decreased")

                if event.type == events.server_start_e:
                    try:
                        self.server = Server()
                        start_new_thread(self.server.boot_up, (num_players,))

                        # self.server = Server(max_players=num_players )
                        self.network = Network()
                        self.network.boot(server=self.server.server, name=name_input.text)

                        return 2  # go to Lobby
                    except:
                        print("failed to create server.")

                if event.type == events.connect_to_server_e:
                    try:
                        server_ip = server_IP_input.text
                        self.network = Network()
                        self.network.boot(server_ip, port=5555, name=name_input.text)
                        return 2  # go to Lobby
                    except:
                        print(
                            "failed to connect to server. Ensure someone else has started a server, and you know their IP Address")

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                # === RENDER ===
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
                # input boxes
                name_input.update(displaysurface)
                server_IP_input.update(displaysurface)

                pygame.display.update()
                FramePerSec.tick(Globals.get_fps())

        return

    def Sim(self, displaysurface):
        '''
        Loop for simulating the game
        :param displaysurface:
        :return:
        '''
        # === SIM ===
        game_model = self.network.send(rules.DataPacket('get'))

        gameboard = GameBoard(game_model)

        game_buttons = pygame.sprite.Group()
        game_buttons.add(Button("test", event=pygame.event.Event(events.test_button_e)))

        all_sprites = pygame.sprite.Group()
        all_sprites.add(gameboard.sprites())
        all_sprites.add(game_buttons.sprites())

        open_spots = []
        required_spots = []
        running = True
        board_tile_select = SelectedTile((0, 0))
        inv_tile_select = SelectedTile((0, 0))
        focus = None
        focus_inv = None
        active_inv_tile = None
        active_board_tile = None
        letters_played = []
        coords_played = []
        turn_start = False
        my_player = game_model.players[self.network.player]

        player_inv_view = Inventory(my_player.Get_Inventory())
        active = False
        # buttons
        commit_btn = Button("commit turn", position=(800, 500), width=150, height=100, event=events.lock_in_e)
        trade_btn = Button("exchange tiles", position=(800, 400), width=150, height=100, event=events.exchange_tiles_e)
        my_turn_button_grp = pygame.sprite.Group([commit_btn, trade_btn])

        while running:
            # prep for frame start
            gameboard.update_from_model(game_model)
            for letter, coord in zip(letters_played, coords_played):
                gameboard.set_tile(letter, coord)
            data = rules.DataPacket('get')
            my_player = game_model.players[self.network.player]
            if self.network.player == game_model.active_player:
                active=True # it is your turn
            else:
                active=False


            if active == True:
                open_spots, required_spots = game_model.Detect_playable_spots()
                if len(required_spots) == 0:
                    required_spots = [(7, 7)]
            else:
                pass
            # update inventory if player just had their turn
            player_inv_view.reset_inventory(my_player.Get_Inventory())

            # mouse is over gameboard
            if gameboard.rect.collidepoint(pygame.mouse.get_pos()):  # only check if within board
                for entity in gameboard:
                    is_hover = entity.rect.collidepoint(pygame.mouse.get_pos())
                    if is_hover:
                        if entity != focus:  # only register a hover event if you hover over a new tile
                            pygame.event.post(pygame.event.Event(events.on_hover_e))
                            focus = entity
            else:  # mouse not over gameboard
                if not board_tile_select.hidden:
                    board_tile_select.hide()

            # mouse is over inventory
            if player_inv_view.rect.collidepoint(pygame.mouse.get_pos()):
                for entity in player_inv_view:
                    is_inv_hover = entity.rect.collidepoint(pygame.mouse.get_pos())
                    if is_inv_hover:
                        if entity != focus_inv:
                            pygame.event.post(pygame.event.Event(events.on_hover_inv_e))
                            focus_inv = entity
                            print("selected new entity!")
            else:  # mouse not over inventory
                if not inv_tile_select.hidden: # hide the selection sprite, but only the first time it notices you arent in inventory.
                    inv_tile_select.hide()

            # ==============+
            # === EVENTS ===|
            # ==============+

            # handle placing a new tile to the board if it is your turn
            if active_board_tile and active_inv_tile and active:
                letters_played.append(active_inv_tile.letter)
                coords_played.append(active_board_tile.coord)
                gameboard.set_tile(active_inv_tile.letter, active_board_tile.coord)
                if active_board_tile.coord in required_spots:
                    particle_target = gameboard.get_tile(active_board_tile.coord).position
                    print("You played a tile in a required spot!")
                    # particle_system.sparkle(particle_target)

                # you placed a tile, so unselect everything
                active_board_tile = None
                active_inv_tile = None

            for event in pygame.event.get():
                for entity in my_turn_button_grp:
                    entity.handle_event(event)
                for entity in gameboard:
                    result, tile = entity.handle_event(event)
                    if result:
                        active_board_tile = tile
                # handle selecting a new inv tile
                for entity in player_inv_view:
                    result, tile = entity.handle_event(event)
                    if result:
                        active_inv_tile = tile

                if event.type == events.on_hover_e:
                    board_tile_select.move(coord=focus.coord)
                if event.type == events.on_hover_inv_e:
                    inv_tile_select.move(position=focus_inv.position)
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
                    print("checking validity...")
                    data = rules.DataPacket(cmd="commit", mode=1, letters_played=letters_played,
                                            coords_played=coords_played, player_id=game_model.active_player)  # create the turn, which the server will process
                    # result = game_model.Process_Turn(data, test=False)
                    # if result == False:
                    #    letters_played = [] # handle a failed commit.
                    #    coords_played = []
                    #    gameboard.update_from_model(game_model)
                    #    print("failed to commit letters")
                    # else:
                    #    print("letters committed successfully! Sending to Server...")
                    #    game_model.Process_Turn(data)
                    #    gameboard.update_from_model(game_model)

                if event.type == events.exchange_tiles_e:
                    if len(letters_played):
                        data = rules.DataPacket('commit', mode=0, letters_played=letters_played, player_id=game_model.active_player)
                    pass

                if event.type == events.game_end_e:
                    # show final results screen
                    # show end game menu
                    pass
                if event.type == events.test_button_e:
                    print("Test button pressed!")
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # === RENDER ===
            displaysurface.fill((0, 0, 0))  # bg (temp)
            # show scoreboard
            self.track_player_status(displaysurface, game_model)

            # update Game Board Tiles
            displaysurface.blit(gameboard.surf, gameboard.rect)  # showing active bounds of board (temp)

            displaysurface.blit(player_inv_view.surf, player_inv_view.rect)

            for entity in gameboard:
                if entity.coord in required_spots:
                    displaysurface.blit(entity.required_surf, entity.required_rect)

                if entity.image:
                    displaysurface.blit(entity.image, entity.rect)
                else:
                    displaysurface.blit(entity.surf, entity.rect)

            if active_inv_tile:
                displaysurface.blit(active_inv_tile.selected_surf, active_inv_tile.selected_rect)
            player_inv_view.update(displaysurface)

            if active_board_tile:
                displaysurface.blit(active_board_tile.selected_surf, active_board_tile.selected_rect)

            if focus:  # Selected tile
                displaysurface.blit(board_tile_select.surf, board_tile_select.rect)
            if focus_inv:
                displaysurface.blit(inv_tile_select.surf, inv_tile_select.rect)

            for entity in my_turn_button_grp:
                entity.update(displaysurface, active=active)

            pygame.display.update()
            FramePerSec.tick(Globals.get_fps())

            # === NETWORK ===
            game_model = self.network.send(data)  # send the data

        return

    def Lobby(self, displaysurface):
        # a temp screen while waiting for players to join the network game.
        # basically, just constantly getting the game_model until all players are present.
        if self.server:
            IP_surf = Globals.get_font(36).render(str(self.server.server), True, (255, 255, 255), (0, 0, 0))
            IP_rect = pygame.Rect((500, 500), (200, 200))
        interval = Globals.get_fps() * 1  # how many times per second should we ask for an update? (save data)
        timer = interval - 1
        cancel_btn = Button(text="Cancel",
                            position=(300, 300),
                            width=200,
                            height=100,
                            font_color=(255, 255, 255),
                            color=(50, 50, 50),
                            color_hover=(70, 70, 70),
                            event=events.cancel_server_e
                            )
        data = rules.DataPacket(cmd='get')
        game_model = self.network.send(data)  # send the data

        while True:
            timer += 1
            # ToDO: A list of names that shows who is in the lobby

            for event in pygame.event.get():
                cancel_btn.handle_event(event)
                if event.type == events.cancel_server_e:
                    return 0

            # === RENDER ===
            displaysurface.fill((0, 0, 0))  # bg (temp)
            if self.server:
                displaysurface.blit(IP_surf, IP_rect)
            cancel_btn.update(displaysurface)
            self.track_player_status(displaysurface, game_model)
            pygame.display.update()
            FramePerSec.tick(Globals.get_fps())
            if timer // interval:
                game_model = self.network.send(rules.DataPacket('get'))
                timer = 0
                if game_model.total_players == len(game_model.players.keys()):
                    return 1

    def track_player_status(self, displaysurface, game_model, my_id=None):
        for player_id in game_model.players.keys():
            me = False
            active = False
            player_data = game_model.players[player_id]
            if player_id == my_id:
                me = True
            if player_id == game_model.active_player:
                active = True
            pos = (Globals.get_width()-200, 300 + (int(player_id) * 100))
            if player_data.name_plate:
                score = player_data.Get_Score
                player_data.name_plate.update(displaysurface, pos, active=active, me=me, score=score)
            else:
                player_data.set_name_plate(NamePlate())

    def Main(self):
        display_surface = pygame.display.set_mode((Globals.get_width(), Globals.get_height()))
        pygame.display.set_caption("Scrabble")

        # setup pre-sim requirements
        # ToDo: Make a Lobby that lets you wait for players to join.
        #game_model = rules.Scrabble()
        #game_model.New_Game()

        # Game Loop
        while True:
            if Globals.get_game_mode() == 0:
                print("game mode is 0")
                Globals.set_game_mode(self.MainMenu(display_surface))
            elif Globals.get_game_mode() == 1:
                print("game mode is 1")
                Globals.set_game_mode(self.Sim(display_surface))
            elif Globals.get_game_mode() == 2:
                Globals.set_game_mode(self.Lobby(display_surface))


if __name__ == '__main__':
    # App Setup
    pygame.init()

    # setup display
    FramePerSec = pygame.time.Clock()

    game = Game()
    game.Main()
