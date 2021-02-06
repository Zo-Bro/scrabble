# would like to move all UI code here so that only the core game loop is in game.py
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
