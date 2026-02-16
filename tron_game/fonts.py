import pygame
from .settings import FONT_PRESS_START, FONT_8BIT_WONDER

def get_title_font(size):
    return pygame.font.Font(str(FONT_PRESS_START), size)

def get_menu_font(size):
    return pygame.font.Font(str(FONT_PRESS_START), size)

def get_hud_font(size):
    return pygame.font.Font(str(FONT_PRESS_START), size)

def get_debug_font(size):
    return pygame.font.Font(str(FONT_8BIT_WONDER), size)

def get_game_over_font(size):
    return pygame.font.Font(str(FONT_PRESS_START), size)
