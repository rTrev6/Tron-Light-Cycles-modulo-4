from pathlib import Path
from arcade_machine_sdk import *
import pygame, random

# Resolución y velocidad
WIDTH = BASE_WIDTH
HEIGHT = BASE_HEIGHT
FPS = DEFAULT_FPS

CELL_SIZE = 7 #Modifica el tamaño, no pasar de 20 porque excederia los bordes al calcular los centros (verificar)
STEP_INTERVAL= 0.03 # Modifica la velocidad

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 100, 0)
RED = (255, 0, 0)
MAGENTA = (200, 60, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
# Colores oscuros
DARK_GRAY = (105, 105, 105)
DARK_RED = (140, 0, 0)
DARK_MAGENTA= (139,0,139)
DARK_BLUE = (0,0,200)

COLORS_VAR= [CYAN, ORANGE, RED, YELLOW, MAGENTA, GREEN, WHITE]

# Controles
DEFAULT_CONTROLS_P1 = {
    "up": pygame.K_w,
    "down": pygame.K_s,
    "left": pygame.K_a,
    "right": pygame.K_d
}

DEFAULT_CONTROLS_P2 = {
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT
}

GAME_DIR = Path(__file__).resolve().parent
CONFIG_FILE = str(GAME_DIR / "controls_config.json")

# Rutas de fuentes usando pathlib
GAME_DIR = Path(__file__).resolve().parent
ASSETS_DIR = GAME_DIR / "assets" 
FONTS_DIR = ASSETS_DIR / "fonts"
IMAGES_DIR = ASSETS_DIR / "images" #Ruta de imagenes
SPRITES_DIR = ASSETS_DIR / "sprites" #Ruta de los sprite
MUSIC_DIR = ASSETS_DIR / "music" #Ruta de la musica
SFX_DIR = ASSETS_DIR / "sfx" #ruta de los efectos de sonido
OBSTACLE_DIR = ASSETS_DIR / "obstacles" #ruta de obstaculos

FONT_PRESS_START = FONTS_DIR / "press start 2p.ttf"
FONT_8BIT_WONDER = FONTS_DIR / "8bit wonder.ttf"
FONT_TR2N = FONTS_DIR / "tr2n.ttf"

BACKGROUND_MENU = IMAGES_DIR / "tron_menu.png" #Fondo menu
SELECTOR = SPRITES_DIR / "moto_cyan.png" #Moto
BACKGROUND_SELECT = IMAGES_DIR / "Tron_menu 2.png" #fondo del seleccion de modo de juego
BACKGROUND_OPTIONS = IMAGES_DIR / "Tron_menu 2.png" #fondo del menu de opciones

# Perfiles de fuente
FONT_FIRST = FONT_TR2N
FONT_TITLE = FONT_PRESS_START
FONT_MENU = FONT_PRESS_START
FONT_HUD = FONT_PRESS_START
FONT_GAME_OVER = FONT_PRESS_START
FONT_DEBUG = FONT_PRESS_START

#Mapeo de colores 
COLOR_NAMES = {
YELLOW: "amarillo",
WHITE: "blanco",
CYAN: "cyan",
MAGENTA: "magenta",
ORANGE: "naranja",
RED: "rojo",
GREEN: "verde",
}

MENU_MUSIC = [
    MUSIC_DIR / "Tron_Music Menu 1.mp3",
    MUSIC_DIR / "Tron_Music Menu 2.mp3",
    MUSIC_DIR / "Tron_Music Menu 3.mp3",
    MUSIC_DIR / "Tron_Music Menu 4.mp3",
    MUSIC_DIR / "Tron_Music Menu 5.mp3"
]
GAME_MUSIC = [
    MUSIC_DIR / "Tron_Music Game 1.mp3",
    MUSIC_DIR / "Tron_Music Game 2.mp3"
]

SFX_COLLISION = SFX_DIR / "collision.mp3"
SFX_GAME_OVER = SFX_DIR / "game_over.mp3"
SFX_BUTTON = SFX_DIR / "button.mp3"
SFX_COUNTDOWN = SFX_DIR / "countdown.mp3"
SFX_START = SFX_DIR / "start.mp3"


def is_valid_obstacle(rect, forbidden_zones):
    return not any(rect.colliderect(zone) for zone in forbidden_zones)

def generate_obstacles(num_obstacles, forbidden_zones, max_attempts=100):
    obstacles = []
    attempts = 0

    while len(obstacles) < num_obstacles and attempts < max_attempts:
        col = random.randint(8, (WIDTH // CELL_SIZE) - 8)
        row = random.randint(8, (HEIGHT // CELL_SIZE) - 8)
        w = random.randint(3, 4)
        h = random.randint(3, 4)

        rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, w * CELL_SIZE, h * CELL_SIZE)

        if is_valid_obstacle(rect, forbidden_zones):
            obstacles.append(rect)

        attempts += 1

    return obstacles