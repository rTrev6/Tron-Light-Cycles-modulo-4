import pygame
from tron_game.state_definitions import State
from tron_game.ui import draw_centered_text, draw_menu_list
from tron_game.settings import WIDTH, HEIGHT, WHITE, CYAN, ORANGE, RED

class GameOverState:
    def __init__(self, game):
        self.game = game

    def enter(self):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.game.reset_game()
                    self.game.state_manager.change(State.COUNTDOWN)
                elif event.key == pygame.K_ESCAPE:
                    self.game.reset_all()
                    self.game.state_manager.change(State.MENU)

    def update(self, dt):
        pass

    def render(self, surface):
        surface.fill((0, 0, 0))
        draw_centered_text(surface, "GAME OVER", self.game.go_font, RED, WIDTH // 2, HEIGHT // 3)

        if self.game.winner == "PLAYER 1":
            draw_centered_text(surface, "GANADOR: PLAYER 1", self.game.menu_font, self.game.player.color, WIDTH // 2, HEIGHT // 3 + 80)
        elif self.game.winner == "PLAYER 2":
            draw_centered_text(surface, "GANADOR: PLAYER 2", self.game.menu_font, self.game.player2.color, WIDTH // 2, HEIGHT // 3 + 80)
        else:
            draw_centered_text(surface, "EMPATE", self.game.menu_font, WHITE, WIDTH // 2, HEIGHT // 3 + 80)

        score_text = f"{self.game.score_p1} - {self.game.score_p2}"
        draw_centered_text(surface, score_text, self.game.menu_font, WHITE, WIDTH // 2, 70)

        draw_menu_list(surface, ["REINTENTAR [ R ]", "SALIR AL MENU [ ESC ]"], self.game.menu_font, WHITE, WIDTH // 2, HEIGHT // 2 + 40, 80)
