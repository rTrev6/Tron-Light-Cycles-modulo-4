import pygame
from tron_game.state_definitions import State
from tron_game.ui import *
from tron_game.settings import *
from tron_game.fonts import *

class GameOverState:
    def __init__(self, game, arcade_mode = False):
        self.game = game
        self.arcade_mode = arcade_mode
        self.selector = None
        self.options = ["REINTENTAR", "SALIR AL MENU"]
        self.selected = 0
        self.buttons = []
        font = self.game.menu_font
        spacing = 60
        base_y = HEIGHT // 2 + 20
        offset = -30

        for i, option in enumerate(self.options):
            text_width, text_height = font.size(option)
            padding_x = 40
            padding_y = 20
            button_width = text_width + padding_x
            button_height = text_height + padding_y
            x = (WIDTH - button_width) // 2
            y = base_y + i * spacing + offset
            self.buttons.append(Button((x, y), (button_width, button_height), GRAY, CYAN))
        
        self.color_timer = 0
       
    def enter(self):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.selected == 0:
                        self.game.reset_game()
                        self.game.state_manager.change(State.COUNTDOWN, self.game, arcade_mode=self.arcade_mode)  # REINICIAR
                    elif self.selected == 1:
                        self.game.reset_all()
                        self.game.play_menu_music() #reiniciar musica
                        self.game.state_manager.change(State.MENU, self.game)  # SALIR AL MENÚ
                elif event.key == pygame.K_ESCAPE:
                    self.game.reset_all()
                    self.game.state_manager.change(State.MENU, self.game)  # También Volver al menu con ESC

    def update(self, dt):
        self.color_timer += dt
        # Alterna cada 0.5 segundos (500 ms)
        if int(self.color_timer * 1) % 2 == 0:
            self.menu_text_color = WHITE
        else:
            self.menu_text_color = BLACK

    def render(self, surface):
        if hasattr(self.game, "last_frame"):
            surface.blit(self.game.last_frame, (0, 0))

        # Superponer capa semitransparente
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)  # Ajusta la opacidad aquí
        overlay.fill((0, 0, 0))  # Color del velo (negro)
        surface.blit(overlay, (0, 0))
        
        if self.selector is None:
            self.selector = pygame.transform.scale(pygame.image.load((SELECTOR)).convert_alpha(), (50,50))
        
        draw_centered_text(surface, "GAME OVER", self.game.go_font, WHITE, WIDTH // 2, HEIGHT // 3)

        if self.game.winner == "PLAYER 1":
            draw_centered_text(surface, "GANADOR: JUGADOR 1", self.game.menu_font, self.game.player.color, WIDTH // 2, HEIGHT // 3 + 80)
        elif self.game.winner == "PLAYER 2":
            draw_centered_text(surface, "GANADOR: JUGADOR 2", self.game.menu_font, self.game.player2.color, WIDTH // 2, HEIGHT // 3 + 80)
        else:
            draw_centered_text(surface, "EMPATE", self.game.menu_font, WHITE, WIDTH // 2, HEIGHT // 3 + 80)

        score_text = f"{self.game.score_p1} - {self.game.score_p2}"
        
        draw_centered_text(surface, score_text, self.game.menu_font, WHITE, WIDTH // 2, 70)

        for i, button in enumerate(self.buttons):
            button.hovered = (i == self.selected)
            button.draw(surface)  # Dibuja primero el botón

        font = self.game.menu_font

        for i, option in enumerate(self.options):
            is_selected = self.buttons[i].hovered
            color = WHITE if is_selected else BLACK

            # Texto centrado en el botón
            text_surface = font.render(option, True, color)
            text_rect = text_surface.get_rect(center=self.buttons[i].rect.center)
            surface.blit(text_surface, text_rect)

                # Flecha a la izquierda si está seleccionado y parpadea cada 0.5s
            if is_selected and int(self.color_timer * 2) % 2 == 0:
                selector_rect = self.selector.get_rect()
                selector_rect.centery = self.buttons[i].rect.centery
                selector_rect.right = self.buttons[i].rect.left - 10
                surface.blit(self.selector, selector_rect)
