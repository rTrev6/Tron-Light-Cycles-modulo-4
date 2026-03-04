import pygame
from pathlib import Path
from tron_game.settings import *

class Player:
    def __init__(self, grid_x, grid_y, color, controls, color_name):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.color = color
        self.color_name = color_name 
        self.direction = None
        self.trail = []
        self.controls = controls
        self.sprites = {}
        self.step_interval = STEP_INTERVAL  # segundos entre pasos
        self.move_timer = 0
        self.fade_trail = False

    def handle_input(self, keys):
        up = self.controls["up"]
        down = self.controls["down"]
        left = self.controls["left"]
        right = self.controls["right"]

        if keys[up] and self.direction != "down":
            self.direction = "up"
        elif keys[down] and self.direction != "up":
            self.direction = "down"
        elif keys[left] and self.direction != "right":
            self.direction = "left"
        elif keys[right] and self.direction != "left":
            self.direction = "right"

    def move(self, dt):
        if self.direction is None:
            return

        self.move_timer += dt
        if self.move_timer >= self.step_interval:
            self.move_timer = 0

            if self.direction == "up":
                self.grid_y -= 1
            elif self.direction == "down":
                self.grid_y += 1
            elif self.direction == "left":
                self.grid_x -= 1
            elif self.direction == "right":
                self.grid_x += 1

            head = (self.grid_x, self.grid_y)
            
            if not self.trail or (self.fade_trail and head != self.trail[-1]["pos"]) or (not self.fade_trail and head != self.trail[-1]):
                if self.fade_trail:
                    self.trail.append({"pos": head, "timestamp": pygame.time.get_ticks()})
                else:
                    self.trail.append(head)


    def check_self_collision(self):
        head = (self.grid_x, self.grid_y)
        if self.fade_trail:
            return any(seg["pos"] == head for seg in self.trail[:-1])
        else:
            return head in self.trail[:-1]

        
    def check_border_collision(self, border_cells=0):
        max_x = WIDTH // CELL_SIZE
        max_y = HEIGHT // CELL_SIZE

        return (
            self.grid_x <= border_cells or
            self.grid_x >= max_x - 1 - border_cells or
            self.grid_y <= border_cells or
            self.grid_y >= max_y - 1 - border_cells
        )
    
    def load_sprites(self):
        """Carga los sprites"""
        try:
            base_dir = Path(__file__).resolve().parent
            sprite_path = base_dir / "assets" / "sprites" / f"moto_{self.color_name}.png"
            base_image = pygame.image.load(str(sprite_path)).convert_alpha()
            base_image = pygame.transform.scale(base_image, (50, 50))

            self.sprites["right"] = base_image
            self.sprites["left"] = pygame.transform.rotate(base_image, 180)
            self.sprites["up"] = pygame.transform.rotate(base_image, 90)
            self.sprites["down"] = pygame.transform.rotate(base_image, 270)
            self.sprites[None] = base_image
        except Exception as e:
            print(f"Error cargando sprite {self.color_name}: {e}")
        
            surf = pygame.Surface((25, 25))
            surf.fill(self.color)
            for d in ["right", "left", "up", "down", None]:
                self.sprites[d] = surf

    def draw(self, surface):
        if not self.sprites:
            self.load_sprites()

    # Dibujar la estela (cada posición es una celda)
        for seg in self.trail:
            if isinstance(seg, dict):
                x, y = seg["pos"]
            else:
                x, y = seg  # Para compatibilidad con modo clásico si es necesario

            rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, self.color, rect)

    
    

    # Obtener imagen rotada
        image = self.sprites.get(self.direction, self.sprites["right"])
        rect = image.get_rect()

    # Coordenadas de la celda actual en píxeles
        cell_x = self.grid_x * CELL_SIZE
        cell_y = self.grid_y * CELL_SIZE

    # Posicionar la moto alineada al frente
        if self.direction == "right":
            rect.center = (cell_x + CELL_SIZE - rect.width / 2,
                       cell_y + CELL_SIZE / 2)
        elif self.direction == "left":
            rect.center = (cell_x + rect.width / 2,
                       cell_y + CELL_SIZE / 2)
        elif self.direction == "up":
            rect.center = (cell_x + CELL_SIZE / 2,
                       cell_y + rect.height / 2)
        elif self.direction == "down":
            rect.center = (cell_x + CELL_SIZE / 2,
                       cell_y + CELL_SIZE - rect.height / 2)
        else:
            rect.center = (cell_x + CELL_SIZE / 2, cell_y + CELL_SIZE / 2)

        surface.blit(image, rect)