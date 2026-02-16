import pygame
from tron_game.settings import *

def draw_centered_text(surface, text, font, color, x, y):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()

    # Compensación visual para fuentes pixeladas
    visual_offset = rect.height * 0.15  
    rect.center = (x, y - visual_offset)

    surface.blit(rendered, rect)

def draw_menu_list(surface, options, font, color, x, start_y, spacing):
    """
    Dibuja una lista de opciones centradas verticalmente.
    options: lista de strings
    font: fuente
    color: color del texto
    x: centro horizontal
    start_y: posición inicial vertical
    spacing: espacio entre líneas
    """
    for i, option in enumerate(options):
        y = start_y + i * spacing
        draw_centered_text(surface, option, font, color, x, y)

class ColorCycler:
    def __init__(self, interval=300):
        self.colors = COLORS_VAR
        self.interval = interval  # ms entre cambios
        self.last_change = pygame.time.get_ticks()
        self.index = 0

    def get_color(self):
        now = pygame.time.get_ticks()
        if now - self.last_change > self.interval:
            self.index = (self.index + 1) % len(self.colors)
            self.last_change = now
        return self.colors[self.index]
