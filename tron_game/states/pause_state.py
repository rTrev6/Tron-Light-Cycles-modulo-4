import pygame
from tron_game.state_definitions import State
from tron_game.ui import *
from tron_game.settings import WIDTH, HEIGHT, WHITE

class PauseState:
    def __init__(self, game, arcade_mode = False):
        self.game = game
        self.arcade_mode = arcade_mode
        self.selector = None
        self.color_timer = 0
        self.options = ["CONTINUAR", "REINICIAR", "SALIR AL MENÚ"]
        self.selected = 0
        self.buttons = []
        font = self.game.menu_font
        spacing = 60
        base_y = HEIGHT // 2
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
        
    def enter(self):
        pass

    def handle_events(self, events):
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.game.sfx_button.play()
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.game.sfx_button.play()
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    self.game.sfx_start.play()
                    if self.selected == 0:
                        self.game.state_manager.change(State.GAME, self.game, arcade_mode = self.arcade_mode)  # CONTINUAR
                    elif self.selected == 1:
                        self.game.reset_game()
                        self.game.state_manager.change(State.COUNTDOWN, self.game, arcade_mode = self.arcade_mode)  # REINICIAR
                    elif self.selected == 2:
                        self.game.state_manager.change(State.MENU, self.game)  # SALIR AL MENÚ
                elif event.key == pygame.K_ESCAPE:
                    self.game.state_manager.change(State.GAME, self.game)  # También CONTINUAR con ESC

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
       
        draw_centered_text(surface, "PAUSA", self.game.title_font, WHITE, WIDTH // 2, HEIGHT // 3)
        
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