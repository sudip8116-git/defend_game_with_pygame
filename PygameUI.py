
import pygame
import random
import math


def isMousePressed(btn_no=0):
    return pygame.mouse.get_pressed()[btn_no]


def rectClick(rect: pygame.Rect):
    return onRect(rect) and isMousePressed()


def onRect(rect):
    return rect.collidepoint(mx(), my())


def mx():
    return pygame.mouse.get_pos()[0]


def my():
    return pygame.mouse.get_pos()[1]


def setCursor(cursor:int):
    pygame.mouse.set_system_cursor(cursor)
    
    
def getDict(**vars):
    return {key:value for key, value in vars.items()}

def parseArgs(var_dict, args):
        for key, value in args:
            var_dict[key] = value
            
def clamp(val, _min, _max):
    if val <  _min:
        val = _min
    if val > _max:
        val = _max
    return val

    

ALL_FONTS = pygame.font.get_fonts()
BUTTONS = []
TEXTS = []
SCROLL_VIEWS = []
SLIDERS = []


class Text:
    '''Draw Text on screen'''

    def __init__(self, screen: pygame.Surface = None, text="New Text", x=0, y=0, **kwargs):
        '''color='black', font_size=20, font_number=10, bold=False, italic=False,
        underline=False, border=False, bg_color=None, bd_color='black', border_width=1
        '''
        self.text = text
        self.screen = screen
        self.pos_x = x
        self.pos_y = y
        self.init_vars()
        parseArgs(self.var_dict, kwargs.items())
        self.font_init()
        if self.var_dict['auto_add']:
            TEXTS.append(self)
        else:
            self.var_dict['border'] = False

    def init_vars(self):
        self.var_dict = getDict(color='black', font_size=20, font_number=10, bold=False, italic=False,
                                underline=False, border=False, bg_color=None, bd_color='black', border_width=1, auto_add=True)

    def font_init(self):
        self.font = pygame.font.SysFont(
            ALL_FONTS[self.var_dict["font_number"]], self.var_dict["font_size"], self.var_dict["bold"], self.var_dict["italic"])

        self.font.underline = self.var_dict["underline"]

        self.text_area = self.font.render(
            self.text, True, self.var_dict['color'])

        self.rect = pygame.Rect(
            0, 0, self.text_area.get_width() + 10, self.text_area.get_height() + 10)

        self.x = self.pos_x - self.text_area.get_width()//2
        self.y = self.pos_y - self.text_area.get_height()//2

        self.rect.topleft = self.x - 5, self.y - 5

    def draw(self):
        if self.var_dict['bg_color']:
            pygame.draw.rect(self.screen, self.var_dict['bg_color'], self.rect)

        if self.var_dict['border']:
            pygame.draw.rect(
                self.screen, self.var_dict['bd_color'], self.rect, self.var_dict['border_width'])

        self.screen.blit(self.text_area, (self.x, self.y))

    def changeText(self, text):
        self.text = text
        self.font_init()

    def changeColor(self, color):
        self.var_dict['color'] = color
        self.text_area = self.font.render(
            self.text, True, color)

    def changePos(self, x, y):
        self.pos_x, self.pos_y = x, y
        self.x = self.pos_x - self.text_area.get_width()//2
        self.y = self.pos_y - self.text_area.get_height()//2
        self.rect.topleft = self.x - 5, self.y - 5


class Button:
    '''A basic Button'''

    def __init__(self, screen: pygame.Surface = None, x=0, y=0, width=100, height=40, text="New Button", **kwargs):
        '''image=None, base_color='white', hover_color='yellow', click_color='green', text_color='black', border_color='black', font_size=20, font_number=10, border_width=2, border=False, image_scale=1, change_cursor=True,
        cursor_id: int = 0
        '''
        self.screen = screen
        self.pos_x = x
        self.pos_y = y
        self.w = width
        self.h = height
        self.is_on = False
        self.surface = pygame.Surface((self.w, self.h))
        self.rect = self.surface.get_rect()
        self.text = Text(self.surface, text, self.w//2,
                         self.h//2, auto_add=False, **kwargs)
        self.init_vars()
        parseArgs(self.var_dict, kwargs.items())
        self.active_color = self.var_dict['base_color']
        self.init_btn()

        BUTTONS.append(self)

    def init_btn(self):
        self.x = self.pos_x - self.w // 2
        self.y = self.pos_y - self.h // 2
        self.rect.topleft = self.x, self.y

    def init_vars(self):
        self.var_dict = getDict(image=None, base_color='gray', hover_color='yellow', click_color='green', text_color='black', border_color='black', font_size=20, font_number=10, border_width=2, border=False, image_scale=1, change_cursor=True,
                                cursor_id=0
                                )

    def draw(self):
        self.check_mouse_hoover()

        self.surface.fill(self.active_color)
        if self.var_dict['image']:
            self.surface.blit(self.var_dict['image'], (0, 0))

        if self.var_dict['border']:
            pygame.draw.rect(self.surface, self.var_dict['border_color'], (
                0, 0, self.w, self.h), self.var_dict['border_width'])

        self.text.draw()

        self.screen.blit(self.surface, (self.x, self.y))

    def check_mouse_hoover(self):
        if onRect(self.rect):
            self.active_color = self.var_dict['hover_color']
            self.is_on = True

        else:
            self.active_color = self.var_dict['base_color']
            self.is_on = False

    def isClick(self) -> bool:
        return isMousePressed() and self.is_on


