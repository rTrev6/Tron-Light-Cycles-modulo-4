from pathlib import Path
from arcade_machine_sdk import *
import pygame

# Resolución y velocidad
WIDTH = BASE_WIDTH
HEIGHT = BASE_HEIGHT
FPS = DEFAULT_FPS


STEP = 10 # Tamaño del jugador y grosor de la estela
SPEED = 300 # Velocidad en píxeles por segundo

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 100, 0)
RED = (255, 0, 0)
MAGENTA = (255, 0, 255)
GREEN = (0, 0, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

COLORS_VAR= [CYAN, ORANGE, RED, BLUE, YELLOW, MAGENTA, GREEN]

# Controles
CONTROLS_P1 = {
    "UP": pygame.K_w,
    "DOWN": pygame.K_s,
    "LEFT": pygame.K_a,
    "RIGHT": pygame.K_d
}

CONTROLS_P2 = {
    "UP": pygame.K_UP,
    "DOWN": pygame.K_DOWN,
    "LEFT": pygame.K_LEFT,
    "RIGHT": pygame.K_RIGHT
}

# Rutas de fuentes usando pathlib
GAME_DIR = Path(__file__).resolve().parent
ASSETS_DIR = GAME_DIR / "assets" / "fonts"

FONT_PRESS_START = ASSETS_DIR / "press start 2p.ttf"
FONT_8BIT_WONDER = ASSETS_DIR / "8bit wonder.ttf"

# Perfiles de fuente
FONT_TITLE = FONT_PRESS_START
FONT_MENU = FONT_PRESS_START
FONT_HUD = FONT_8BIT_WONDER
FONT_GAME_OVER = FONT_PRESS_START
FONT_DEBUG = FONT_8BIT_WONDER

# Colores cíclicos para el título
TITLE_COLORS = [
    (0, 200, 255),  # azul neón
    (255, 0, 255),  # magenta
    (0, 255, 150),  # verde cian
    (255, 100, 0),  # Orange
    (0, 0, 255),    # Blue
    (255, 0, 0),    # Red
    (255, 255, 0)   #Yellow
]
