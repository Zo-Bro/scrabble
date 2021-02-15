import sys
import os
from uuid import uuid4
from _thread import *

import pygame
from pygame.locals import *

from player import Letter
from network import Network
from server import Server
import events
import rules


class GlobalVars:
    """
    All the variables that need to be accessible by any function or class
    """

    def __init__(self):
        # System Settings
        self._HEIGHT = 720
        self._WIDTH = 1080
        self._FPS = 60

        # Board Dimensions
        self._TILE_SIZE = 32
        self._BORDER_SIZE = 4
        self._BOARD_OFFSET = (450, 25)

        # Font
        self._FONT = 'Cambria'

        # Game Controls
        self._GAME_MODE = 0

        # Colors
        self._MENU_COLOR = (25,25,25)
        self._SELECTED_TILE_COLOR = (158, 235, 52)
        self._ACTIVE_COLOR = (218, 234, 240)
        self._INACTIVE_COLOR = (119, 155, 168)
        self._REQUIRED_TILE_COLOR = (50, 155, 168)
        self._FONT_COLOR = (35, 80, 97)
        self._HIGHLIGHT_COLOR = (250, 206, 60)
        self._BG_COLOR = ()
        self._TILE_COLOR = 'cream'
        self._3W_COLOR = 'red'
        self._2W_COLOR = 'pink'
        self._3L_COLOR = 'dark_blue'
        self._2L_COLOR = 'blue'
        self._CENTER_COLOR = 'gold'
        self._special_color_dict = {
            (3, 'w'): self._3W_COLOR,
            (2, 'w'): self._2W_COLOR,
            (3, 'l'): self._3L_COLOR,
            (2, 'l'): self._2L_COLOR,
            (1,'l'): self._CENTER_COLOR,
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

    def get_menu_color(self):
        return self._MENU_COLOR



Globals = GlobalVars()


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
        self.tiles = {}
        self.icons128 = {}
        self.icons256 = {}
        self.panels = {}
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
                self.numbers[num_name] = image
        for root, dirs, files in os.walk(r"images\bgs"):
            for item in files:
                item_name = os.path.splitext(item)[0]
                item_name = item_name.rsplit('_')[0]
                image = pygame.image.load(os.path.join(root, item))
                self.bgs[item_name] = image
        for root, dirs, files in os.walk(r"images\buttons"):
            for btn in files:
                btn_name = os.path.splitext(btn)[0]
                image = pygame.image.load(os.path.join(root, btn))
                self.buttons[btn_name] = image
        for root, dirs, files in os.walk(r"images\tiles"):
            for tile in files:
                tile_name = os.path.splitext(tile)[0]
                self.tiles[tile_name] = pygame.image.load(os.path.join(root, tile))
        for root, dirs, files in os.walk(r'images\icons\icons_128'):
            for icon in files:
                icon_name = os.path.splitext(icon)[0]
                self.icons128[icon_name] = pygame.image.load(os.path.join(root, icon))
        for root, dirs, files in os.walk(r'images\icons\icons_256'):
            for icon in files:
                icon_name = os.path.splitext(icon)[0]
                self.icons256[icon_name] = pygame.image.load(os.path.join(root, icon))
        for root, dirs, files in os.walk(r'images\inner_panels'):
            for item in files:
                item_name = os.path.splitext(item)[0]
                self.panels[item_name] = pygame.image.load(os.path.join(root, item))

IMAGES = Images()

class NamePlate(pygame.sprite.Sprite):
    '''
    An Image displaying a players name
    '''
    WIDTH = 200
    HEIGHT = 50
    def __init__(self, name='', id=None):
        self.width = 200
        self.height = 50
        self.rect = pygame.Rect((0, 0), (self.width, self.height))
        self.color = Globals.get_inactive_color()
        self.font_color = (255, 255, 255)
        self.font_size = 20
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill(self.color)
        self.name = name
        self.id = id
        self.text = name
        self.text_surface = Globals.get_font(self.font_size).render(self.text, True, self.font_color)

    def set_name(self, name):
        self.name = name
        self.text = name
        self.text_surface = Globals.get_font(self.font_size).render(self.text, True, self.font_color)

    def update(self, displaysurface, position, active=False, me=False, score=None):
        if score:
            text = self.name + ": " + str(score)
            text_surface = Globals.get_font(self.font_size).render(text, True, self.font_color)
        else:
            text_surface = self.text_surface

        self.rect.update(position, (self.width, self.height))
        displaysurface.blit(self.surf, self.rect)
        displaysurface.blit(text_surface, (self.rect.x, self.rect.y))
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
        self.surf = pygame.Surface((width, height))
        self.rect = self.surf.get_rect(center=position)
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
                self.surf.fill(self.color)
            else:
                self.active = False
                self.color = Globals.get_inactive_color()
                self.surf.fill(self.color)

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
        displaySurface.blit(self.surf, self.rect)
        #pygame.draw.rect(displaySurface, self.color, self.rect)
        self.text_surface = Globals.get_font(self.font_size).render(self.text, True, self.font_color)
        displaySurface.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))

        return


class PopUp:
    """
    a window that holds other widgets.
    """

    def __init__(self, position=(100, 100), width=300, height=200):
        self.position = position
        self.width = width
        self.height = height
        self.surf = pygame.Surface((self.width, self.height), position)
        self.rect = pygame.Rect(self.position, (self.width, self.height))
        # self.close_event = pygame.event.

    def handle_event(self):
        pass


class TextBox():
    """
    An easy way to render text to the screen
    """

    def __init__(self, text='',
                 position=(100, 100),
                 width=300,
                 height=100,
                 font_color=(255, 255, 255),
                 font_size=12,
                 window_style=None,
                 color='blue',
                 button='ok'):
        font = Globals.get_font(font_size)
        self.text = font.render(text, True, font_color)
        self.text_rect = self.text.get_rect(center=position)
        self.position = position
        self.width = width
        self.height = height
        self.surf = pygame.Surface((self.width, self.height))
        self.win_style = [WindowNormal, WindowTileHolder]
        if window_style:
            self.window = self.win_style[window_style](position, width, height, color)
        else:
            self.window = None


    def set_image(self, image):
        size = (self.width, self.height)
        if image.get_size()[0] > self.width or image.get_size()[1] > self.height:
            image = pygame.transform.smoothscale(image, size)
            self.image = image
            self.surf.fill(self.color)
        return

    def update(self, displaysurface):
        if self.window:
            self.window.update(displaysurface)
        displaysurface.blit(self.text, self.text_rect)


class WindowFrame(pygame.sprite.Sprite):
    def __init__(self,
                 position=(Globals.get_height() / 2, Globals.get_width() / 2),
                 width=20,
                 height=20,
                 color='blue'):
        super().__init__()
        font = Globals.get_font(35)
        self.color = color
        self.surf = pygame.surface.Surface((width, height))
        self.surf.fill(color)
        self.position = position
        self.make_image_from_pieces(width, height)

    def make_image_from_pieces(self, w, h, color='green'):
        left_corn = ''
        left_edge = '_button_left_edge'
        mid = '_button_middle'
        right_edge = '_button_right_edge'

        self.left_img = IMAGES.buttons[color + left_edge].copy()
        edge_size = self.left_img.get_size()
        # self.left_img = pygame.transform.smoothscale(self.left_img, (edge_size[0], h))

        self.mid_img = IMAGES.buttons[color + mid].copy()
        # self.mid_img = pygame.transform.smoothscale(self.mid_img, (w-edge_size[0], h))
        self.mid_img = pygame.transform.smoothscale(self.mid_img, (w - edge_size[0], self.mid_img.get_size()[1]))

        self.right_img = IMAGES.buttons[color + right_edge].copy()
        # self.right_img = pygame.transform.smoothscale(self.right_img, (edge_size[0], h))

        l_size = self.left_img.get_size()
        r_size = self.right_img.get_size()
        m_size = self.mid_img.get_size()

        self.l_surf = pygame.surface.Surface(self.left_img.get_size())
        self.mid_surf = pygame.surface.Surface(self.mid_img.get_size())
        self.r_surf = pygame.surface.Surface(self.right_img.get_size())

        self.l_rect = self.l_surf.get_rect(center=(self.position[0] - (w / 2), self.position[1]))
        self.mid_rect = self.mid_surf.get_rect(center=self.position)
        self.r_rect = self.r_surf.get_rect(center=(self.position[0] + (w / 2), self.position[1]))
        self.height = self.mid_img.get_size()[1]

        # highlighted version of pieces.
        self.h_l_img = self.left_img.copy()
        self.h_l_img.fill((20, 20, 20), special_flags=pygame.BLEND_ADD)
        self.h_r_img = self.right_img.copy()
        self.h_r_img.fill((20, 20, 20), special_flags=pygame.BLEND_ADD)
        self.h_m_img = self.mid_img.copy()
        self.h_m_img.fill((20, 20, 20), special_flags=pygame.BLEND_ADD)

        # create rect from image dimensions
        full_size = (l_size[0] + r_size[0] + m_size[0], l_size[1])
        full_surf = pygame.Surface(full_size)
        self.rect = full_surf.get_rect(center=self.position)
        # self.h_l_img = self.


class Button(pygame.sprite.Sprite):
    """
    A Clickable Button bound to a specific event
    inherits from Sprite so it can be added to groups easily.
    """

    def __init__(self, text='',
                 position=(Globals.get_height() / 2, Globals.get_width() / 2),
                 width=20,
                 height=20,
                 font_color=(0, 0, 0, 100),
                 color='green',
                 event=events.dummy_e):
        super().__init__()
        font = Globals.get_font(35)
        self.color = color
        self.text = font.render(text, True, font_color)
        self.text_rect = self.text.get_rect(center=position)
        self.surf = pygame.surface.Surface((width, height))
        self.position = position
        self.event = event
        self.state = 'neutral'
        self._hidden = False
        self.make_gui(width, height, color)

    def make_gui(self, w, h, color='green'):
        left_edge = '_button_left_edge'
        mid = '_button_middle'
        right_edge = '_button_right_edge'
        self.left_img = IMAGES.buttons[color + left_edge].copy()
        edge_size = self.left_img.get_size()
        # self.left_img = pygame.transform.smoothscale(self.left_img, (edge_size[0], h))

        self.mid_img = IMAGES.buttons[color + mid].copy()
        # self.mid_img = pygame.transform.smoothscale(self.mid_img, (w-edge_size[0], h))
        self.mid_img = pygame.transform.smoothscale(self.mid_img, (w - edge_size[0], self.mid_img.get_size()[1]))

        self.right_img = IMAGES.buttons[color + right_edge].copy()
        # self.right_img = pygame.transform.smoothscale(self.right_img, (edge_size[0], h))

        l_size = self.left_img.get_size()
        r_size = self.right_img.get_size()
        m_size = self.mid_img.get_size()

        self.l_surf = pygame.surface.Surface(self.left_img.get_size())
        self.mid_surf = pygame.surface.Surface(self.mid_img.get_size())
        self.r_surf = pygame.surface.Surface(self.right_img.get_size())

        self.l_rect = self.l_surf.get_rect(center=(self.position[0] - (w / 2), self.position[1]))
        self.mid_rect = self.mid_surf.get_rect(center=self.position)
        self.r_rect = self.r_surf.get_rect(center=(self.position[0] + (w / 2), self.position[1]))
        self.height = self.mid_img.get_size()[1]

        # highlighted version of pieces.
        self.h_l_img = self.left_img.copy()
        self.h_l_img.fill((20, 20, 20), special_flags=pygame.BLEND_ADD)
        self.h_r_img = self.right_img.copy()
        self.h_r_img.fill((20, 20, 20), special_flags=pygame.BLEND_ADD)
        self.h_m_img = self.mid_img.copy()
        self.h_m_img.fill((20, 20, 20), special_flags=pygame.BLEND_ADD)

        # create rect from image dimensions
        full_size = (l_size[0] + r_size[0] + m_size[0], l_size[1])
        full_surf = pygame.Surface(full_size)
        self.rect = full_surf.get_rect(center=self.position)
        # self.h_l_img = self.

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
            display_surface.blit(self.mid_img, self.mid_rect)
            display_surface.blit(self.left_img, self.l_rect)
            display_surface.blit(self.right_img, self.r_rect)
            if self.state == 'hover':
                display_surface.blit(self.h_m_img, self.mid_rect)
                display_surface.blit(self.h_l_img, self.l_rect)
                display_surface.blit(self.h_r_img, self.r_rect)
            display_surface.blit(self.text, self.text_rect)

    def hover(self):
        if self.state == 'neutral':
            self.state = 'hover'

        else:
            pass

    def neutral(self):
        if self.state != 'neutral':
            self.state = 'neutral'

    def inactive(self):
        if self.state != 'inactive':
            self.state = 'inactive'
            self.surf.fill(Globals.get_inactive_color())

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.state == 'hover':
                pygame.event.post(pygame.event.Event(self.event))

class RoundButton(pygame.sprite.Sprite):
    def __init__(self, text='',
                 image=None,
                 position=(Globals.get_height() / 2, Globals.get_width() / 2),
                 scale=1.0,
                 font_color=(0, 0, 0, 100),
                 color='green',
                 event=events.dummy_e):
        super().__init__()
        font = Globals.get_font(35)
        self.image = image
        image_size = self.image.get_size()
        new_size = (int(image_size[0]*scale), int(image_size[1]*scale))
        self.image = pygame.transform.smoothscale(self.image, new_size)
        self.image_rect = self.image.get_rect(center=position)

        self.color = color
        self.text = font.render(text, True, font_color)
        self.text_rect = self.text.get_rect(center=position)
        self.position = position
        self.event = event
        self.state = 'neutral'
        self._hidden = False
        self.make_gui(scale, color)

    def make_gui(self, scale, color='green'):
        name = color + '_round_button'
        self.up_img = IMAGES.buttons[name].copy()
        image_size = self.up_img.get_size()
        new_size = (int(image_size[0]*scale), int(image_size[1]*scale))
        self.up_img = pygame.transform.smoothscale(self.up_img, new_size)
        self.h_img = self.up_img.copy()
        self.h_img.fill((70,70,70), special_flags=pygame.BLEND_ADD)
        self.inactive_img = self.up_img.copy()
        self.inactive_img.fill((20,20,20), special_flags=pygame.BLEND_MULT)
        self.rect = self.up_img.get_rect(center=self.position)

    def hide(self, hide_bool=True):
        self._hidden = hide_bool

    def update(self, display_surface, active=True):
        if not self._hidden:
            if not active:
                display_surface.blit(self.inactive_img, self.rect)
            elif self.rect.collidepoint(pygame.mouse.get_pos()):
                self.hover()
            else:
                self.neutral()
            display_surface.blit(self.up_img, self.rect)

            if self.state == 'hover':
                display_surface.blit(self.h_img, self.rect)

            if self.image:
                display_surface.blit(self.image, self.image_rect)
            else:
                display_surface.blit(self.text, self.text_rect)

    def hover(self):
        if self.state == 'neutral':
            self.state = 'hover'

        else:
            pass

    def neutral(self):
        if self.state != 'neutral':
            self.state = 'neutral'

    def inactive(self):
        if self.state != 'inactive':
            self.state = 'inactive'


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
            image = pygame.transform.smoothscale(image, self.custom_size)
        else:
            self.custom_size = image.get_size()
        self.surf = pygame.Surface(image.get_size())
        self.rect = self.surf.get_rect(center=position)
        self.image = image

    def set_image(self, image):
        self.image = pygame.transform.smoothscale(image, self.custom_size)


def invert_coord_y(coord):
    x = coord[0]
    y = coord[1]
    y = 14 - y
    return x, y

class Window:
    def __init__(self, position=(0,0), width=300, height=500, color='blue'):
        self.pos = position
        self.width = width
        self.height = height
        self.color = color
        self.make_gui()

    def make_gui(self, color,  style):
        pass
    def update(self):
        pass

class WindowNormal(Window):
    def __init__(self, position=(0,0), width=100, height=100, color='blue'):
        super().__init__(position, width, height, color)
    def add_vector(self, coord_1 = (), coord_2 = ()):
        '''
        Vector Addition
        :param coord_1:
        :param coord_2:
        :return:
        '''
        x = coord_1[0] + coord_2[0]
        y = coord_1[1] + coord_2[1]
        return (x,y)

    def make_gui(self):
        base = self.color + '_inner_panel_nine_{}'

        nine_panel_names = ['patch_top_left', 'patch_top_center', 'patch_top_right',
                            'patch_left_center', 'patch_center', 'patch_right_center',
                            'patch_bottom_left', 'patch_bottom_center', 'patch_bottom_right', ]

        bar_names = ['bar_left_edge', 'bar_center_repeating', 'bar_right_edge']
        self.images = []
        self.images.append(IMAGES.panels[base.format(nine_panel_names[0])].copy())
        self.images.append(IMAGES.panels[base.format(nine_panel_names[1])].copy())
        self.images.append(IMAGES.panels[base.format(nine_panel_names[2])].copy())

        self.images.append( IMAGES.panels[base.format(nine_panel_names[3])].copy())
        self.images.append( IMAGES.panels[base.format(nine_panel_names[4])].copy())
        self.images.append( IMAGES.panels[base.format(nine_panel_names[5])].copy())

        self.images.append( IMAGES.panels[base.format(nine_panel_names[6])].copy())
        self.images.append( IMAGES.panels[base.format(nine_panel_names[7])].copy())
        self.images.append( IMAGES.panels[base.format(nine_panel_names[8])].copy())

        # size of each
        self.sizes = []
        for item in self.images:
            self.sizes.append(item.get_size())

        #resize middle parts of edges, and center
        corner_w = self.sizes[0][0]
        corner_h = self.sizes[0][1]

        # top center

        self.images[1] = pygame.transform.smoothscale(self.images[1], (max(1, self.width-corner_w*2), self.sizes[1][1]))

        # center left edge
        self.images[3] = pygame.transform.smoothscale(self.images[3], (self.sizes[3][0], max(1, self.height-(corner_h*2))))

        # center
        self.images[4] = pygame.transform.smoothscale(self.images[4], (max(1,self.width-(corner_w*2)), max(1,self.height-(corner_h*2))))


        # center right edge
        self.images[5] = pygame.transform.smoothscale(self.images[5], (self.sizes[5][0], max(1,self.height-(corner_h*2))))

        # bottom center
        self.images[7] = pygame.transform.smoothscale(self.images[7], (max(1,self.width-corner_w*2), self.sizes[7][1]))


        # surf
        self.surfaces = []
        for item in self.images:
            self.surfaces.append(pygame.Surface(item.get_size()))
        # subtract width, subtract height
        t_l_pos = self.add_vector(((-self.width/2) + (self.sizes[0][0]/2), (-self.height/2) + (self.sizes[0][1]/2)), self.pos)
        t_l_rect = self.surfaces[0].get_rect(center=t_l_pos)

        # top center = no change width, subtract height
        t_c_pos = self.add_vector((0, (-self.height/2) + (self.sizes[1][1]/2)), self.pos)
        t_c_rect = self.surfaces[1].get_rect(center=t_c_pos)

        # top right = ADD width, subtract height
        t_r_pos = self.add_vector(((self.width/2) - (self.sizes[2][0]/2), (-self.height/2) + (self.sizes[2][1]/2)), self.pos)

        t_r_rect = self.surfaces[2].get_rect(center=t_r_pos)

        # mid left = Subtract Width, no change to height
        l_c_pos = self.add_vector(((-self.width/2) + (self.sizes[3][0]/2), 0), self.pos)
        l_c_rect = self.surfaces[3].get_rect(center=l_c_pos)

        c_rect = self.surfaces[4].get_rect(center=self.pos)
        # mid right = add width, no chang eheight
        r_c_pos = self.add_vector(((self.width/2) - (self.sizes[5][0]/2), 0), self.pos)
        r_c_rect = self.surfaces[5].get_rect(center=r_c_pos)

        # bot left = sub width, add height
        b_l_pos = self.add_vector(((-self.width/2) + (self.sizes[6][0]/2), (self.height/2) - (self.sizes[6][1]/2)), self.pos)
        b_l_rect = self.surfaces[6].get_rect(center=b_l_pos)

        # bot mid = no change width, add height
        b_c_pos = self.add_vector((0, (self.height/2) - (self.sizes[7][1]/2)), self.pos)
        b_c_rect = self.surfaces[7].get_rect(center=b_c_pos)

        # bot right = add width, add height
        b_r_pos = self.add_vector(((self.width/2) - (self.sizes[8][0]/2), (self.height/2) - (self.sizes[8][1]/2)), self.pos)
        b_r_rect = self.surfaces[0].get_rect(center=b_r_pos)

        self.rects = [t_l_rect,t_c_rect,t_r_rect,
                      l_c_rect, c_rect, r_c_rect,
                      b_l_rect, b_c_rect, b_r_rect]

    def update(self, displaysurface):
        for image, rect in zip(self.images, self.rects):
            displaysurface.blit(image, rect)

class WindowTileHolder(Window):
    def __init__(self, position=(0,0), width=300, height=500, color='blue'):
        super().__init__(position, width, height, color)
    def add_vector(self, coord_1 = (), coord_2 = ()):
        '''
        Vector Addition
        :param coord_1:
        :param coord_2:
        :return:
        '''
        x = coord_1[0] + coord_2[0]
        y = coord_1[1] + coord_2[1]
        return (x,y)

    def make_gui(self):
        base = self.color + '_tile_holder_{}'

        panel_names = ['top_left', 'top_repeating', 'top_right',
                            'left_repeating', 'center', 'right_repeating',
                            'bottom_left', 'bottom_repeating', 'bottom_right', ]

        bar_names = ['bar_left_edge', 'bar_center_repeating', 'bar_right_edge']
        self.images = []
        self.images.append(IMAGES.panels[base.format(panel_names[0])].copy())
        self.images.append(IMAGES.panels[base.format(panel_names[1])].copy())
        self.images.append(IMAGES.panels[base.format(panel_names[2])].copy())

        self.images.append( IMAGES.panels[base.format(panel_names[3])].copy())
        self.images.append( IMAGES.panels[base.format(panel_names[4])].copy())
        self.images.append( IMAGES.panels[base.format(panel_names[5])].copy())

        self.images.append( IMAGES.panels[base.format(panel_names[6])].copy())
        self.images.append( IMAGES.panels[base.format(panel_names[7])].copy())
        self.images.append( IMAGES.panels[base.format(panel_names[8])].copy())

        # size of each
        self.sizes = []
        for item in self.images:
            self.sizes.append(item.get_size())

        #resize middle parts of edges, and center
        corner_w = self.sizes[0][0]
        corner_h = self.sizes[0][1]

        # top center

        self.images[1] = pygame.transform.smoothscale(self.images[1], (max(1, self.width-corner_w*2), self.sizes[1][1]))

        # center left edge
        self.images[3] = pygame.transform.smoothscale(self.images[3], (self.sizes[3][0], max(1, self.height-(corner_h*2))))

        # center
        self.images[4] = pygame.transform.smoothscale(self.images[4], (max(1,self.width-(corner_w*2)), max(1,self.height-(corner_h*2))))


        # center right edge
        self.images[5] = pygame.transform.smoothscale(self.images[5], (self.sizes[5][0], max(1,self.height-(corner_h*2))))

        # bottom center
        self.images[7] = pygame.transform.smoothscale(self.images[7], (max(1,self.width-corner_w*2), self.sizes[7][1]))


        # surf
        self.surfaces = []
        for item in self.images:
            self.surfaces.append(pygame.Surface(item.get_size()))
        # subtract width, subtract height
        t_l_pos = self.add_vector(((-self.width/2) + (self.sizes[0][0]/2), (-self.height/2) + (self.sizes[0][1]/2)), self.pos)

        t_l_rect = self.surfaces[0].get_rect(center=t_l_pos)

        # top center = no change width, subtract height
        t_c_pos = self.add_vector((0, (-self.height/2) + (self.sizes[1][1]/2)), self.pos)
        t_c_rect = self.surfaces[1].get_rect(center=t_c_pos)

        # top right = ADD width, subtract height
        t_r_pos = self.add_vector(((self.width/2) - (self.sizes[2][0]/2), (-self.height/2) + (self.sizes[2][1]/2)), self.pos)

        t_r_rect = self.surfaces[2].get_rect(center=t_r_pos)

        # mid left = Subtract Width, no change to height
        l_c_pos = self.add_vector(((-self.width/2) + (self.sizes[3][0]/2), 0), self.pos)
        l_c_rect = self.surfaces[3].get_rect(center=l_c_pos)

        c_rect = self.surfaces[4].get_rect(center=self.pos)
        # mid right = add width, no chang eheight
        r_c_pos = self.add_vector(((self.width/2) - (self.sizes[5][0]/2), 0), self.pos)
        r_c_rect = self.surfaces[5].get_rect(center=r_c_pos)

        # bot left = sub width, add height
        b_l_pos = self.add_vector(((-self.width/2) + (self.sizes[6][0]/2), (self.height/2) - (self.sizes[6][1]/2)), self.pos)
        b_l_rect = self.surfaces[6].get_rect(center=b_l_pos)

        # bot mid = no change width, add height
        b_c_pos = self.add_vector((0, (self.height/2) - (self.sizes[7][1]/2)), self.pos)
        b_c_rect = self.surfaces[7].get_rect(center=b_c_pos)

        # bot right = add width, add height
        b_r_pos = self.add_vector(((self.width/2) - (self.sizes[8][0]/2), (self.height/2) - (self.sizes[8][1]/2)), self.pos)
        b_r_rect = self.surfaces[0].get_rect(center=b_r_pos)

        self.rects = [t_l_rect,t_c_rect,t_r_rect,
                      l_c_rect, c_rect, r_c_rect,
                      b_l_rect, b_c_rect, b_r_rect]

    def update(self, displaysurface):
        for image, rect in zip(self.images, self.rects):
            displaysurface.blit(image, rect)

class Tile(pygame.sprite.Sprite):
    """
    creates a rectangular sprite for each playable tile.
    the self.coord is only used when the tile is on the game board.

    """

    def __init__(self, coord=None, invLetter=None, color=(50,50,50), tile_image='cream', position=(0, 0), letter_uuid=None, scale=1):
        super().__init__()
        tile_size = Globals.get_tile_size() * scale
        border_size = Globals.get_border_size()
        board_offset = Globals.get_board_offset()
        self.uuid = uuid4()
        self.tapped = False
        self.scale = scale
        self.visible = True
        self.surf = pygame.Surface((tile_size, tile_size))
        self.color = color

        if coord:  # placed on board
            coord = invert_coord_y(coord)
            border_x = tile_size / border_size * coord[0]
            border_y = tile_size / border_size * coord[1]
            self.position = (tile_size * coord[0] + border_x + board_offset[0],
                             tile_size * coord[1] + border_y + board_offset[1])  # y
            self.rect = self.surf.get_rect(topleft=self.position)
            self.coord = coord
        else:  # not placed on board
            self.position = position
            self.rect = self.surf.get_rect(topleft=self.position)

        # an overlay that shows selection
        selection_img = IMAGES.tiles['select_border_white']
        selection_img = pygame.transform.smoothscale(selection_img, (tile_size + border_size * 2, tile_size + border_size * 2))
        self.selected_surf = selection_img.copy()
        #self.selected_surf = pygame.Surface((tile_size + border_size * 2, tile_size + border_size * 2))
        self.selected_surf.fill(Globals.get_selected_tile_color(), special_flags=BLEND_MULT)
        self.selected_surf.set_alpha(128)
        self.selected_rect = self.selected_surf.get_rect(
            topleft=(self.position[0], self.position[1]))

        # a box that renders beneath the tile which shows if its a required spot
        self.required_surf = selection_img.copy()
        #self.required_surf = pygame.Surface((tile_size + border_size * 2, tile_size + border_size * 2))
        self.required_surf.fill(Globals.get_required_tile_color(), special_flags=pygame.BLEND_MULT)
        self.highlight_rect = self.selected_surf.get_rect(
            topleft=(self.position[0] - border_size, self.position[1] - border_size))

        self.tapped_surf = selection_img.copy()
        #self.tapped_surf = pygame.Surface((tile_size + border_size * 2, tile_size + border_size * 2))
        self.tapped_surf.fill((0,255,0), special_flags=pygame.BLEND_MULT)
        self.tapped_surf.set_alpha(128)
        self.tapped_rect = self.tapped_surf.get_rect(
            topleft=(self.position[0]-border_size, self.position[1]-border_size))

        # set up the letter image it has a letter placed
        if invLetter is not None:
            self.letter_uuid = invLetter.uuid
            self.set_image(invLetter)
        else:
            self.letter_uuid = None
            self.letter_img = None
            self.letter = None
        self.tile_img = IMAGES.tiles[tile_image + '_thin_border']
        if self.tile_img.get_size()[0] > tile_size or self.tile_img.get_size()[1] > tile_size:
            self.tile_img = pygame.transform.smoothscale(self.tile_img, (tile_size, tile_size))

    def set_image(self, invLetter=None, letter=None):
        tile_size = Globals.get_tile_size()
        letter_value = {       'a':1,
                                    'b':3,
                                    'c':3,
                                    'd':2,
                                    'e':1,
                                    'f':4,
                                    'g':2,
                                    'h':4,
                                    'i':1,
                                    'j':8,
                                    'k':5,
                                    'l':1,
                                    'm':3,
                                    'n':1,
                                    'o':1,
                                    'p':3,
                                    'q':10,
                                    'r':1,
                                    's':1,
                                    't':1,
                                    'u':3,
                                    'v':4,
                                    'w':4,
                                    'x':8,
                                    'y':4,
                                    'z':10
                                    }
        if invLetter:
            self.letter = invLetter.letter
            image = IMAGES.letters[invLetter.letter]
            self.letter_uuid = invLetter.uuid
            score_val = letter_value[invLetter.letter]
        elif letter:
            self.letter = letter
            image = IMAGES.letters[letter]
            self.letter_uuid = None
            score_val = letter_value[letter]
        score_val = str(score_val)
        self.number_img = IMAGES.numbers[score_val]
        self.number_img = pygame.transform.smoothscale(self.number_img, (int(tile_size*self.scale/5), int(tile_size*self.scale/5)))
        num_size = self.number_img.get_size()
        pos = self.position
        pos = (pos[0]+tile_size*self.scale - num_size[0]-2, pos[1]+tile_size*self.scale - num_size[1]-2)
        self.number_rect = self.number_img.get_rect(center=pos)
        if image.get_size()[0] > tile_size or image.get_size()[1] > tile_size*self.scale:
            image = pygame.transform.smoothscale(image, (tile_size*self.scale, tile_size*self.scale))

        self.letter_img = image

        return

    def handle_event(self, event):
        '''
        if you click this tile, set a highlight around it and then return itself
        :param event:
        :return:
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not self.tapped:
                    if self.rect.collidepoint(pygame.mouse.get_pos()):
                        return True, self
        return False, None

    def reset(self):
        self.letter_img = None

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False
    def tap(self, tapped=True):
        self.tapped = tapped
    def update(self, displaysurface):
        if self.visible:
            if self.letter_img:
                displaysurface.blit(self.tile_img, self.rect)
                displaysurface.blit(self.letter_img, self.rect)
                displaysurface.blit(self.number_img, self.number_rect)

            else:
                displaysurface.blit(self.tile_img, self.rect)
            if self.tapped:
                displaysurface.blit(self.tapped_surf, self.rect)
    def set_position(self, new_position):
        self.position = new_position
        tile_size = Globals.get_tile_size()
        self.rect = self.surf.get_rect(topleft=self.position)
        if self.number_img:
            num_size = self.number_img.get_size()
            pos = self.position
            pos = (pos[0]+tile_size*self.scale - num_size[0]-2, pos[1]+tile_size*self.scale - num_size[1]-2)
            self.number_rect = self.number_img.get_rect(center=pos)



class SelectedTile(Tile):
    def __init__(self, coord, scale=1):
        super().__init__(coord, color=Globals.get_highlight_color())
        size = (Globals.get_tile_size()*scale + (Globals.get_border_size() * 2),
                                    Globals.get_tile_size()*scale + (Globals.get_border_size() * 2))
        self.surf = pygame.Surface(size)
        self.image = IMAGES.tiles['tile_face']
        self.image = pygame.transform.smoothscale(self.image, size)
        #self.image.fill((30,30,30), special_flags=pygame.BLEND_ADD)
        self.image.set_alpha(128)
        self.surf.fill(self.color)
        self.surf.set_alpha(128)
        self.hidden = True

    def move(self, coord=None, position=None):
        if position:
            tile_size = Globals.get_tile_size()
            border_size = Globals.get_border_size()
            board_offset = Globals.get_board_offset()
            self.hidden = False
            self.rect.update(position, (tile_size-border_size, tile_size-border_size))
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

    def update(self, displaysurface):
        if not self.hidden:
            #displaysurface.blit(self.surf, self.rect)
            displaysurface.blit(self.image, self.rect)


class Inventory(pygame.sprite.Group):
    '''
    Display  for the tiles in a player's inventory.
    '''

    def __init__(self, letters=[]):
        super().__init__()
        self.bounds_buffer = 20
        self.scale = 2
        self.tile_size = Globals.get_tile_size() * self.scale

        self.border_size = Globals.get_border_size()
        board_offset = Globals.get_board_offset()
        height = Globals.get_height()
        width = 700
        self.bounds = (
            7 * (self.tile_size + self.border_size),
            self.tile_size + self.border_size)  # x = 7 tiles wide with some buffer, y = 2 tiles tall
        self.position = (25, (height - height / 10))  # x = close to left edge, y = close to  bottom edge
        self.surf = pygame.surface.Surface(self.bounds)
        self.surf.fill((50, 50, 50, 100))
        self.rect = self.surf.get_rect(topleft=self.position)
        self.reset_inventory(letters, first_time=True)
        self.uuid_dict = self.create_uuid_dict()

    def create_uuid_dict(self):
        uuid_dict = {}
        if len(self.sprites()):
            for tile in self.sprites():
                uuid_dict[str(tile.letter_uuid)] = tile
        return uuid_dict

    def reset_inventory(self, invLetters, first_time = False):
        if first_time:
            self.empty()
            for index, letter in enumerate(invLetters):
                position = (
                    self.position[0] + index * (self.tile_size + self.border_size), self.position[1]
                )
                self.add(Tile(invLetter=letter, position=position, scale=self.scale))
        else:
            new_letter_uuids = [str(x.uuid) for x in invLetters]
            existing_letter_uuids = [str(x.letter_uuid) for x in self.sprites()]
            tiles_to_remove = []
            for old_id in existing_letter_uuids:
                if old_id not in new_letter_uuids:
                    tiles_to_remove.append(self.uuid_dict[old_id])
            self.remove(tiles_to_remove)
            for index, new_id in enumerate(new_letter_uuids):
                if new_id not in existing_letter_uuids:
                    self.add_tile(invLetters[index], index=index)
            self.uuid_dict = self.create_uuid_dict()
            self.recalc_positions()
            #for new_letter in invLetters:
            #    self.add_tile(new_letter)

    def recalc_positions(self):
        for index, tile in enumerate(self.sprites()):
            position = (
                self.position[0] + index * (self.tile_size + self.border_size), self.position[1]
            )
            tile.set_position(position)

    def remove_tile(self, letter):
        tile_to_remove = None
        for tile in self.sprites():
            if tile.letter_uuid == letter.uuid: # if this GUI represents the letter in the model, remove it
                tile_to_remove = tile
                break
        if tile_to_remove is not None:
            self.remove(tile_to_remove)
            return True
        else:
            return False
    def add_tile(self, letter, index=None):
        if index ==None:
            index = len(self.sprites())
            if index >= 7:
                return False
        index -= 1
        position = (
            self.position[0] + index * (Globals.get_tile_size() + Globals.get_border_size()), self.position[1]
        )
        self.add(Tile(invLetter=letter, position=position, scale=self.scale))
        return True

    def update(self, displaysurface):
        for tile in self.sprites():
            tile.update(displaysurface)

class WordQCounter:
    def __init__(self, position, count, font_size=20, font_color=(255,255,255)):
        self.font = Globals.get_font(font_size)
        self.font_color = font_color
        self.count = count
        self.label = self.font.render("Tiles Left:", True, font_color)
        self.label_rect = self.label.get_rect(center=position)
        label_height = self.label.get_height()
        self.text = self.font.render(str(count), True, font_color)
        text_pos = (position[0], position[1]+label_height)
        self.text_rect= self.text.get_rect(center=text_pos)

    def update(self, displaysurface, count):
        if self.count != count:
            self.text =self.font.render(str(count), True, self.font_color)
        displaysurface.blit(self.label, self.label_rect)
        displaysurface.blit(self.text, self.text_rect)

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
                    tile_image = Globals.get_special_color(special_tiles[coord_code])
                else:
                    tile_image = Globals.get_tile_color()
                tileSlot = Tile((c_index, r_index), tile_image=tile_image)
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

    def set_tile(self, letter=None, coord=(0, 0)):
        '''
        makes the tile at the given coords render the given letter
        :param coord:
        :param image:
        :return:
        '''
        tile = self.get_tile(coord)

        if letter:
            tile.set_image(letter=letter)
            return True
        else:
            tile.reset()
        return False

    def update_from_model(self, game_model):
        playboard = game_model.Get_Playboard()
        for y, column in enumerate(playboard):
            for x, value in enumerate(column):
                self.set_tile(value, (x, y))

    def update(self, displaysurface, required_spots):

        for entity in self.sprites():
            if entity.coord in required_spots:
                displaysurface.blit(entity.required_surf, entity.highlight_rect)
            entity.update(displaysurface)


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
        grid_bg_1 = ImageSprite(image=IMAGES.bgs['grid'],
                                   position=(500, 500)
                                   )
        grid_bg_2 = ImageSprite(image=IMAGES.bgs['grid'],
                                   position=(1000, 500)
                                   )
        self.grids_grp = pygame.sprite.Group([grid_bg_1, grid_bg_2])


    def MainMenu(self, displaysurface):
        # main menu buttons
        num_players = 2
        name_text = ''
        host_window = WindowNormal(position=((Globals.get_width() / 2)-200, (Globals.get_height() / 2)+100), width=400, height=500, color='blue')
        join_window = WindowNormal(position=((Globals.get_width() / 2)+200, (Globals.get_height() / 2)+100), width=400, height=500, color='blue')

        #round_btn = RoundButton(image=IMAGES.icons128['cross'], scale=0.2, color='pink')
        player_minus_btn = RoundButton(text="",
                                       image=IMAGES.icons128['minus'],
                                       position=((Globals.get_width() / 2)-200-60, Globals.get_height() / 2),
                                       scale=0.25,
                                       color='green',
                                       event=events.decrease_players_e
                                  )
        player_plus_btn = RoundButton(text="",
                                      image=IMAGES.icons128['add'],
                                      position=((Globals.get_width() / 2)-200+60, Globals.get_height() / 2),
                                      scale=0.25,
                                      event=events.increase_players_e
                                 )
        server_btn = Button(text="Host Server",
                            position=((Globals.get_width() / 2)-200, Globals.get_height() - 150),
                            width=250,
                            height=50,
                            event=events.server_start_e)

        join_btn = Button(text="Join Game",
                          position=((Globals.get_width() / 2)+200, Globals.get_height() - 150),
                          width=250,
                          height=50,
                          event=events.connect_to_server_e
                          )

        main_menu_buttons = pygame.sprite.Group([server_btn, join_btn])

        main_menu_buttons.add([player_minus_btn, player_plus_btn])

        # text input
        name_input_label = TextBox(text="Name:", position=(Globals.get_width()/2-175,150 ),width=100, height=50, font_size=36)
        name_input = TextInput(position=(Globals.get_width()/2,150 ), default_text='<enter name>')
        server_IP_input = TextInput(position=((Globals.get_width() / 2)+200, Globals.get_height() / 2),
                                    width=250,
                                    height=50,
                                    font_size=36,
                                    max_chars=36,
                                    default_text='192.168.1.12'
                                    )
        # main menu sprites
        main_menu_bg = ImageSprite(image=IMAGES.bgs['blue'],
                                   position=(Globals.get_width() / 2, Globals.get_height() / 2),
                                   set_custom_size=(Globals.get_width(), Globals.get_height())
                                   )
        player_count_image = ImageSprite(image=IMAGES.numbers[str(num_players)],
                                         position=((Globals.get_width() / 2)-200, Globals.get_height() / 2),
                                         set_custom_size=(50, 50)
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
                        player_count_image.set_image(IMAGES.numbers[str(num_players)])

                if event.type == events.decrease_players_e:
                    if num_players > 2:
                        num_players -= 1
                        player_count_image.set_image(IMAGES.numbers[str(num_players)])

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
                for entity in self.grids_grp:
                    displaysurface.blit(entity.image, entity.rect)
                # windows
                host_window.update(displaysurface)
                join_window.update(displaysurface)

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
                name_input_label.update(displaysurface)
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
        all_sprites = pygame.sprite.Group()
        all_sprites.add(gameboard.sprites())
        all_sprites.add(game_buttons.sprites())

        open_spots = []
        required_spots = []
        running = True

        # selection and cursor tracking
        board_tile_select = SelectedTile((0, 0))
        inv_tile_select = SelectedTile((0, 0), scale=2)
        focus = None
        focus_inv = None
        active_inv_tile = None
        active_board_tile = None

        # tiles played this turn
        letters_played = []
        coords_played = []

        #  your player and inventory
        my_player = game_model.players[self.network.player]
        player_inv_view = Inventory(my_player.Get_Inventory())

        # game states (trading letters state, etc)
        swap_view = False

        # buttons
        #commit_btn_pos = (Globals.get_board_offset()[0]+((Globals.get_tile_size()+Globals.get_border_size())*8), Globals.get_height()-50)
        commit_btn_pos = (275, Globals.get_height()-125)
        commit_btn = RoundButton(image=IMAGES.icons128['cursor_right'], position=commit_btn_pos, scale=0.5, color='green', event=events.lock_in_e)
        trade_btn_pos = (100, Globals.get_height()-125)
        trade_btn = RoundButton(image=IMAGES.icons128['replay'], position=trade_btn_pos, scale=0.4, color='red', event=events.exchange_tiles_e)
        remove_btn_pos = (175, Globals.get_height()-125)
        remove_placed_btn = RoundButton(image=IMAGES.icons128['rewind'], position=remove_btn_pos, scale=0.4, color='yellow', event=events.remove_tile_e)
        my_turn_button_grp = pygame.sprite.Group([commit_btn, trade_btn, remove_placed_btn])
        ok_pos = player_inv_view.position
        ok_pos= (ok_pos[0] + player_inv_view.rect.w, ok_pos[1]+player_inv_view.rect.h/4)
        #ok_pos = (ok_pos[0] + 36*7, ok_pos[1])
        cancel_pos= (ok_pos[0], ok_pos[1]+(player_inv_view.rect.h/4)*3)
        ok_btn = RoundButton("", image=IMAGES.icons128['tick'], position=ok_pos, scale=0.2, color='green', event=events.commit_swap_e)
        cancel_btn = RoundButton(image=IMAGES.icons128['cross'], position=cancel_pos, scale=0.2, color='red', event=events.exchange_tiles_e)
        swap_tiles_button_grp = pygame.sprite.Group([ok_btn, cancel_btn])

        # other GUI
        swap_view_text_box = TextBox(text='Swap Which Tiles?', window_style=1, color='orange')
        name_plates = self.create_name_plates(game_model)
        wordQcounter = WordQCounter((50, Globals.get_height()-125), game_model.Get_WordQ_Len())

        while running:
            # prep for frame start
            gameboard.update_from_model(game_model)
            for letter, coord in zip(letters_played, coords_played):
                gameboard.set_tile(letter.letter, coord)
            data = rules.DataPacket('get')
            if game_model.players[self.network.player].Get_Inventory_UUIDs() != my_player.Get_Inventory_UUIDs():
                my_player = game_model.players[self.network.player]
                player_inv_view.reset_inventory(my_player.Get_Inventory(), first_time=False)
                for tile in player_inv_view.sprites():
                    tile.tap(False)

            if self.network.player == game_model.active_player:
                open_spots, required_spots = game_model.Detect_playable_spots(coords_played)
                if len(required_spots) == 0:
                    required_spots = [(7, 7)]
            else:
                open_spots, required_spots = [], []
                letters_played, coords_played = [], []
            # update inventory if player just had their turn
            #inv_model = my_player.Get_Inventory()
            #player_inv_view.reset_inventory(inv_model)

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
            else:  # mouse not over inventory
                if not inv_tile_select.hidden:  # hide the selection sprite, but only the first time it notices you arent in inventory.
                    inv_tile_select.hide()

            # ==========================================================================================================
            # === EVENTS ===============================================================================================
            # ==========================================================================================================

            # handle placing a new tile to the board if it is your turn
            if active_board_tile and active_inv_tile and game_model.active_player == self.network.player \
                    and active_board_tile.coord in required_spots and swap_view == False:

                letters_played.append(my_player.Get_Letter_by_UUID(active_inv_tile.letter_uuid))
                coords_played.append(active_board_tile.coord)
                gameboard.set_tile(active_inv_tile.letter, active_board_tile.coord)
                for tile in player_inv_view.sprites():
                    if tile.letter_uuid == active_inv_tile.letter_uuid:
                        tile.tap(True)
                #active_inv_tile.tap(True)
                if active_board_tile.coord in required_spots:
                    particle_target = gameboard.get_tile(active_board_tile.coord).position
                    print("You played a tile in a required spot!")
                    # particle_system.sparkle(particle_target)

                # you placed a tile, so unselect everything
                active_board_tile = None
                active_inv_tile = None

            # handle selecting multiple letters from inventory if swap mode is active
            elif active_inv_tile and game_model.active_player == self.network.player and swap_view == True:
                if len(letters_played):
                    if not active_inv_tile.tapped:
                        letters_played.append(my_player.Get_Letter_by_UUID(active_inv_tile.letter_uuid))
                else:
                    letters_played.append(my_player.Get_Letter_by_UUID(active_inv_tile.letter_uuid))
                for tile in player_inv_view.sprites():
                    if tile.letter_uuid == active_inv_tile.letter_uuid:
                        tile.tap(True)
                # you placed a tile, so unselect everything
                active_board_tile = None
                active_inv_tile = None


            for event in pygame.event.get():
                for entity in my_turn_button_grp:
                    entity.handle_event(event)
                if swap_view:
                    for entity in swap_tiles_button_grp:
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
                    inv_tile_select.move(position=(focus_inv.position[0]-Globals.get_border_size(), focus_inv.position[1]-Globals.get_border_size()))
                if event.type == events.remove_tile_e:
                    for letter_tile in player_inv_view:
                        letter_tile.tap(False)
                    letters_played = []
                    for coord in coords_played:
                        gameboard.set_tile('', coord)
                    coords_played = []

                if event.type == events.turn_end_e:
                    # give control to next player
                    # reload the tiles of the just finished player
                    pass
                if event.type == events.lock_in_e:
                    data = rules.DataPacket(cmd="commit", mode=1, letters_played=letters_played,
                                            coords_played=coords_played,
                                            player_id=game_model.active_player)  # create the turn, which the server will process
                    for inv_tile in player_inv_view:
                        inv_tile.tap(False)
                if event.type == events.exchange_tiles_e:
                    # run a sub-loop that lets the player select multiple tiles,
                    # and then click OK or Cancel to exit the loop
                    # all selected letters are put into letters_played

                    #remove all tiles from board
                    print("Swap View Toggled")
                    swap_view = not swap_view
                    print("swap_view is :" + str(swap_view))
                    for letter_tile in player_inv_view:
                        letter_tile.tap(False)
                    letters_played = []
                    for coord in coords_played:
                        gameboard.set_tile('', coord)
                    coords_played = []

                if event.type == events.commit_swap_e:
                    if len(letters_played) and swap_view == True:
                        data = rules.DataPacket('commit', mode=0, letters_played=letters_played,
                                                player_id=game_model.active_player)
                        pygame.event.post(pygame.event.Event(events.exchange_tiles_e))

                if event.type == events.game_end_e:
                    # show final results screen
                    # show end game menu
                    pass
                if event.type == events.test_button_e:
                    print("Test button pressed!")
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # ==========================================================================================================
            # === RENDER ===============================================================================================
            # ==========================================================================================================

            displaysurface.fill((0, 0, 0))  # bg (temp)
            for entity in self.grids_grp:
                displaysurface.blit(entity.image, entity.rect)
            # show scoreboard
            self.track_player_status(displaysurface, game_model, name_plates, self.network.player)
            wordQcounter.update(displaysurface, game_model.Get_WordQ_Len())
            # show current player's turn
            active_player_text = Globals.get_font(20).render(str(game_model.players[game_model.active_player].name) +'s Turn', True, (255,255,255))
            displaysurface.blit(active_player_text, active_player_text.get_rect(topleft=(100, 50)))
            # update Game Board Tiles
            displaysurface.blit(gameboard.surf, gameboard.rect)  # showing active bounds of board (temp)

            displaysurface.blit(player_inv_view.surf, player_inv_view.rect)
            gameboard.update(displaysurface, required_spots)

            '''
            for entity in gameboard:
            if entity.coord in required_spots:
                displaysurface.blit(entity.required_surf, entity.highlight_rect)
            entity.update(displaysurface)
            '''

            if active_inv_tile:
                displaysurface.blit(active_inv_tile.selected_surf, active_inv_tile.highlight_rect)
            player_inv_view.update(displaysurface)

            if active_board_tile:
                displaysurface.blit(active_board_tile.selected_surf, active_board_tile.highlight_rect)

            if focus:  # Selected tile
                board_tile_select.update(displaysurface)
                #displaysurface.blit(board_tile_select.surf, board_tile_select.rect)
            if focus_inv:
                inv_tile_select.update(displaysurface)
                #displaysurface.blit(inv_tile_select.surf, inv_tile_select.rect)

            for entity in my_turn_button_grp:  # turn control buttons
                entity.update(displaysurface, active=game_model.active_player == self.network.player)
            if swap_view:
                swap_view_text_box.update(displaysurface)
                for entity in swap_tiles_button_grp:
                    entity.update(displaysurface, active=game_model.active_player == self.network.player)

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
                            color='green',
                            event=events.cancel_server_e
                            )
        data = rules.DataPacket(cmd='get')
        game_model = self.network.send(data)  # send the data
        name_plates = self.create_name_plates(game_model)
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
            self.add_name_plate(game_model, name_plates)
            self.track_player_status(displaysurface, game_model, name_plates)
            pygame.display.update()
            FramePerSec.tick(Globals.get_fps())
            if timer // interval:
                game_model = self.network.send(rules.DataPacket('get'))
                timer = 0
                if game_model.total_players == len(game_model.players.keys()):
                    return 1

    def create_name_plates(self, game_model):
        name_plates = {}
        for player_id in game_model.players.keys():
            player_data = game_model.players[player_id]
            name_plates[player_id] = NamePlate(name=player_data.name, id=player_data.Get_ID())
        return name_plates

    def add_name_plate(self, game_model, name_plates):
        if len(game_model.players.keys()) > len(name_plates.keys()):

            for player_id in game_model.players.keys():
                if player_id not in name_plates.keys():
                    player_data = game_model.players[player_id]
                    name_plates[player_id] = NamePlate(name=player_data.name, id=player_data.Get_ID())
        return name_plates

    def track_player_status(self, displaysurface, game_model, name_plates, my_id=None):
        for player_id in game_model.players.keys():
            me = False
            active = False
            player_data = game_model.players[player_id]
            if player_id == my_id:
                me = True
            if player_id == game_model.active_player:
                active = True
            #pos = (Globals.get_width() - NamePlate.WIDTH, 300 + (int(player_id) * NamePlate.HEIGHT))
            pos = (0, 100 + (int(player_id) * NamePlate.HEIGHT))

            score = player_data.Get_Score()
            name_plates[player_id].update(displaysurface, pos, active=active, me=me, score=score)

    def Main(self):
        display_surface = pygame.display.set_mode((Globals.get_width(), Globals.get_height()))
        pygame.display.set_caption("Scrabble")

        # setup pre-sim requirements
        # ToDo: Make a Lobby that lets you wait for players to join.
        # game_model = rules.Scrabble()
        # game_model.New_Game()

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
