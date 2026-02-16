import pygame
from tron_game.state_definitions import State
from tron_game.ui import draw_centered_text, draw_menu_list
from tron_game.settings import WIDTH, HEIGHT, WHITE

class PauseState:
    def __init__(self, game):
        self.game = game

    def enter(self):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.game.state_manager.change(State.GAME)
                elif event.key == pygame.K_ESCAPE:
                    self.game.state_manager.change(State.MENU)

    def update(self, dt):
        pass

    def render(self, surface):
        draw_centered_text(surface, "PAUSA", self.game.title_font, WHITE, WIDTH // 2, HEIGHT // 4)
        draw_menu_list(surface, ["CONTINUAR [ P ]", "SALIR AL MENU [ ESC ]"], self.game.menu_font, WHITE, WIDTH // 2, HEIGHT // 2, 45)
        self.game.player.draw(surface)
        self.game.player2.draw(surface)
