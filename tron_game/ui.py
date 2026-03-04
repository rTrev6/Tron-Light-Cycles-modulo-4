import pygame
import math
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

class Button:
    def __init__(self, pos, size, color, border_color):
        
        self.pos = pos
        self.size = size
        self.color = color
        self.border_color = border_color
        self.rect = pygame.Rect(pos, size)
        

    def draw(self, surface):
      
        pygame.draw.rect(surface, self.color, self.rect, border_radius=6)
        pygame.draw.rect(surface, self.border_color, self.rect, border_radius=6, width = 3)
        
#Halo alrededor de la cuadricula de juego

def draw_game_grid(surface, color, spacing=40, thickness=1):
    width, height = surface.get_size()

    for x in range(0, width, spacing):
        pygame.draw.line(surface, color, (x, 0), (x, height), thickness)

    for y in range(0, height, spacing):
        pygame.draw.line(surface, color, (0, y), (width, y), thickness)
        

def draw_glowing_border_frame(surface, color=(255, 0, 255), time=0, thickness=2, glow_layers=3, border_width=40):
    width, height = surface.get_size()

    for layer in range(glow_layers):
        alpha = int(150 / (layer + 1)) #modificar 150 lo hace mas intenso
        glow_color = (*color, alpha)
        glow_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        pulse = int(2 * math.sin(time * 2 + layer))

        # Rectángulo interior del marco
        inner_rect = pygame.Rect(
            border_width - layer * 2,
            border_width - layer * 2,
            width - 2 * (border_width - layer * 2),
            height - 2 * (border_width - layer * 2)
        )

        pygame.draw.rect(glow_surface, glow_color, inner_rect, thickness + pulse)
        surface.blit(glow_surface, (0, 0))


def draw_glowing_obstacle(surface, rect, outer_color, inner_color, glow_thickness=4):
    # Borde exterior
    pygame.draw.rect(surface, outer_color, rect)

    # Borde interior (más pequeño)
    inner_rect = rect.inflate(-glow_thickness, -glow_thickness)
    if inner_rect.width > 0 and inner_rect.height > 0:
        pygame.draw.rect(surface, inner_color, inner_rect)



def draw_help_overlay(surface, title_font, text_font, alpha=220):
    overlay_width = WIDTH - 200
    overlay_height = HEIGHT - 200
    overlay_x = 100
    overlay_y = 100

    # Fondo atenuado
    darken = pygame.Surface((WIDTH, HEIGHT))
    darken.set_alpha(100)
    darken.fill((0, 0, 0))
    surface.blit(darken, (0, 0))

    # Ventana de ayuda
    overlay = pygame.Surface((overlay_width, overlay_height))
    overlay.set_alpha(int(alpha))
    overlay.fill((20, 20, 20))
    surface.blit(overlay, (overlay_x, overlay_y))

    pygame.draw.rect(surface, GRAY, (overlay_x, overlay_y, overlay_width, overlay_height), 4)

    draw_centered_text(surface, "¿CÓMO JUGAR?", title_font, WHITE, WIDTH // 2, overlay_y + 80)

    instrucciones = [
        "Jugador 1: Use W A S D para moverse",
        "Jugador 2: Use las flechas para moverse",
        "Evita chocar con las paredes o estelas",
        "El último jugador en pie gana",
        "",
        "Presiona ESC para volver al menu"
    ]

    for i, linea in enumerate(instrucciones):
        y = overlay_y + 100 + i * 60
        draw_centered_text(surface, linea, text_font, WHITE, WIDTH // 2, y +40)
