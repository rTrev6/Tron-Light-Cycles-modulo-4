import pygame
from tron_game.state_definitions import State
from tron_game.ui import draw_centered_text, draw_menu_list
from tron_game.settings import WIDTH, HEIGHT, WHITE

class MenuState:
    def __init__(self, game):
        self.game = game

    def enter(self):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.game.reset_game()
                    self.game.state_manager.change(State.COUNTDOWN)
                elif event.key == pygame.K_ESCAPE:
                    self.game.stop()

    def update(self, dt):
        pass

    def render(self, surface):
        color = self.game.title_anim.get_color()
        draw_centered_text(surface, "TRON", self.game.title_font, color, WIDTH // 2, HEIGHT // 4)
        draw_centered_text(surface, "LIGHT CYCLES", self.game.title_font, color, WIDTH // 2, HEIGHT // 4 + 80)
        draw_menu_list(surface, ["JUGAR [ SPACE ]", "OPCIONES [ O ]", "SALIR [ ESC ]"], self.game.menu_font, WHITE, WIDTH // 2, HEIGHT // 2, 80)
