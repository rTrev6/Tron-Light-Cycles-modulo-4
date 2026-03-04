import pygame
from tron_game.state_definitions import State
from tron_game.ui import *
from tron_game.settings import *
from tron_game.grid_effects import *

class GameState:
    def __init__(self, game, arcade_mode = False):
        self.game = game
        self.arcade_mode = arcade_mode
        self.trail_lifetime = 5000 #ms, duracion de la estela en modo arcade.
        self.obstacles = []          # lista de rectángulos de obstáculos
        self.obstacle_sprites = []   # lista de superficies (sprites) para cada obstáculo
        self.obstacle_dir = GAME_DIR / "assets" / "sprites" / "obstacles" 
        
    def enter(self):
    
        if self.arcade_mode:
            self.game.player.fade_trail = True
            self.game.player2.fade_trail = True

            margin = 6 * CELL_SIZE
            hud_height = 100

            forbidden_zones = []

            hud_zone = pygame.Rect(0, 0, WIDTH, hud_height)
            forbidden_zones.append(hud_zone)

            p1_zone = pygame.Rect(
                self.game.player.grid_x * CELL_SIZE - margin,
                self.game.player.grid_y * CELL_SIZE - margin,
                CELL_SIZE + 2 * margin,
                CELL_SIZE + 2 * margin
            )
            forbidden_zones.append(p1_zone)

            p2_zone = pygame.Rect(
                self.game.player2.grid_x * CELL_SIZE - margin,
                self.game.player2.grid_y * CELL_SIZE - margin,
                CELL_SIZE + 2 * margin,
                CELL_SIZE + 2 * margin
            )
            forbidden_zones.append(p2_zone)

            self.obstacles = generate_obstacles(num_obstacles=15, forbidden_zones=forbidden_zones)
            self.obstacle_sprites = []
            sprite_paths = []
            if self.obstacle_dir.exists():
                sprite_paths = list(self.obstacle_dir.glob("*.png")) + list(self.obstacle_dir.glob("*.jpg"))

            for obs in self.obstacles:
                if sprite_paths:
                    # Elegir un sprite aleatorio y escalarlo al tamaño del obstáculo
                    path = random.choice(sprite_paths)
                    try:
                        sprite = pygame.image.load(str(path)).convert_alpha()
                        sprite = pygame.transform.scale(sprite, (obs.width, obs.height))
                        self.obstacle_sprites.append(sprite)
                    except Exception as e:
                        print(f"Error cargando sprite de obstáculo: {e}")
                        surf = pygame.Surface((obs.width, obs.height), pygame.SRCALPHA)
                        surf.fill((255, 0, 255, 128)) 
                        self.obstacle_sprites.append(surf)
                else:
                    # No hay sprites: crear superficie de color como fallback
                    surf = pygame.Surface((obs.width, obs.height), pygame.SRCALPHA)
                    surf.fill((255, 0, 255, 128))  
                    self.obstacle_sprites.append(surf)
        else:
            # Modo clásico: sin obstáculos
            self.obstacles = []
            self.obstacle_sprites = []
    
        self.game.play_game_music()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.game.last_frame = self.game.surface.copy()
                self.game.state_manager.change(State.PAUSE, self.game, arcade_mode=self.arcade_mode)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    self.game.current_track_index = (self.game.current_track_index + 1) % len(self.game.menu_music_paths)
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(self.game.menu_music_paths[self.game.current_track_index])
                    pygame.mixer.music.play(-1)          
                
    def update(self, dt):
        
        keys = pygame.key.get_pressed()
        self.game.player.handle_input(keys)
        self.game.player.move(dt)
        self.game.player2.handle_input(keys)
        self.game.player2.move(dt)
        
        if self.arcade_mode:
            p1_trail_positions = [seg["pos"] for seg in self.game.player.trail]
            p2_trail_positions = [seg["pos"] for seg in self.game.player2.trail]
        else:
            p1_trail_positions = self.game.player.trail
            p2_trail_positions = self.game.player2.trail
        
        if self.arcade_mode:
            now = pygame.time.get_ticks()
            for player in [self.game.player, self.game.player2]:
                if player.fade_trail:
                    player.trail = [seg for seg in player.trail if seg["timestamp"] is not None and now - seg["timestamp"] < self.trail_lifetime]


        p1_head = (self.game.player.grid_x, self.game.player.grid_y)
        p2_head = (self.game.player2.grid_x, self.game.player2.grid_y)
        
        p1_dead = (
            self.game.player.check_self_collision() or
            self.game.player.check_border_collision() or
            p1_head in p2_trail_positions
        )
        p2_dead = (
            self.game.player2.check_self_collision() or
            self.game.player2.check_border_collision() or
            p2_head in p1_trail_positions
        )


        if self.arcade_mode:
            
            p1_rect = pygame.Rect(self.game.player.grid_x * CELL_SIZE, self.game.player.grid_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            p2_rect = pygame.Rect(self.game.player2.grid_x * CELL_SIZE, self.game.player2.grid_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            p1_dead = p1_dead or any(p1_rect.colliderect(obs) for obs in self.obstacles)
            p2_dead = p2_dead or any(p2_rect.colliderect(obs) for obs in self.obstacles)
                               

                
        if p1_dead and p2_dead:
            self.game.winner = "EMPATE"
        elif p1_dead:
            self.game.winner = "PLAYER 2"
            self.game.score_p2 += 1
        elif p2_dead:
            self.game.winner = "PLAYER 1"
            self.game.score_p1 += 1

        if p1_dead or p2_dead:
            pygame.mixer.music.stop()
            
            self.game.sfx_collision.play()
            
            self.game.last_frame = self.game.surface.copy()
            self.game.sfx_game_over.play()
            self.game.state_manager.change(State.GAME_OVER, self.game, arcade_mode=self.arcade_mode)
            self.game.fadeout_music(400)


    def render(self, surface):
        
        draw_game_grid(surface, 
                       GRAY, 
                       spacing=40, 
                       thickness=2)

        draw_glowing_border_frame(surface, color=CYAN, time=pygame.time.get_ticks() / 1000, thickness=6, glow_layers=5, border_width=10)
            
        draw_centered_text(surface, "JUGADOR 1", self.game.menu_font, self.game.player.color, 160, 40)
        draw_centered_text(surface, "JUGADOR 2", self.game.menu_font, self.game.player2.color, WIDTH - 140, 40)

        if self.game.game_start_time:
            elapsed = (pygame.time.get_ticks() - self.game.game_start_time) // 1000
            minutes = elapsed // 60
            seconds = elapsed % 60
            time_text = f"{minutes:02}:{seconds:02}"
            draw_centered_text(surface, time_text, self.game.menu_font, WHITE, WIDTH // 2, 40)

        score_text = f"{self.game.score_p1} - {self.game.score_p2}"
        draw_centered_text(surface, score_text, self.game.menu_font, WHITE, WIDTH // 2, 70)
        
        if self.arcade_mode:
            for i, obs in enumerate(self.obstacles):
                if i < len(self.obstacle_sprites):
                    surface.blit(self.obstacle_sprites[i], obs.topleft)


        if self.arcade_mode:
            self._draw_fading_trail(surface, self.game.player)
            self._draw_fading_trail(surface, self.game.player2)
        else:
            for seg in self.game.player.trail:
                if isinstance(seg, tuple) and len(seg) == 2:
                    x, y = seg
                    pygame.draw.rect(surface, self.game.player.color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            for seg in self.game.player2.trail:
                if isinstance(seg, tuple) and len(seg) == 2:
                    x, y = seg
                    pygame.draw.rect(surface, self.game.player2.color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        self.game.player.draw(surface)
        self.game.player2.draw(surface)
        
        if self.arcade_mode:
            if int(pygame.time.get_ticks() / 500) % 2 == 0:
                draw_centered_text(surface, "MODO ARCADE", self.game.menu_font, ORANGE, WIDTH // 2, HEIGHT - 30)

    def _draw_fading_trail(self, surface, player):
        now = pygame.time.get_ticks()
        for seg in player.trail:
            x, y = seg["pos"]
            timestamp = seg["timestamp"]

            if timestamp is not None:
                age = now - timestamp
                alpha = max(30, 255 - int(255 * (age / self.trail_lifetime)))
            else:
                alpha = 255  # Estela sólida en modo clásico

            trail_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            trail_surface.fill((*player.color, alpha))
            surface.blit(trail_surface, (x * CELL_SIZE, y * CELL_SIZE))

      