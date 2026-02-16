import pygame
from tron_game.state_definitions import State
from tron_game.ui import draw_centered_text
from tron_game.settings import WIDTH, HEIGHT, STEP, CYAN, ORANGE, WHITE

class GameState:
    def __init__(self, game):
        self.game = game

    def enter(self):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.game.state_manager.change(State.PAUSE)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.game.player.handle_input(keys)
        self.game.player.move(dt)
        self.game.player2.handle_input(keys)
        self.game.player2.move(dt)

        p1_head = (round(self.game.player.x / STEP) * STEP, round(self.game.player.y / STEP) * STEP)
        p2_head = (round(self.game.player2.x / STEP) * STEP, round(self.game.player2.y / STEP) * STEP)

        p1_dead = (
            self.game.player.check_self_collision() or
            self.game.player.out_of_bounds() or
            p1_head in self.game.player2.trail
        )
        p2_dead = (
            self.game.player2.check_self_collision() or
            self.game.player2.out_of_bounds() or
            p2_head in self.game.player.trail
        )

        if p1_dead and p2_dead:
            self.game.winner = "EMPATE"
        elif p1_dead:
            self.game.winner = "PLAYER 2"
            self.game.score_p2 += 1
        elif p2_dead:
            self.game.winner = "PLAYER 1"
            self.game.score_p1 += 1

        if p1_dead or p2_dead:
            self.game.state_manager.change(State.GAME_OVER)

    def render(self, surface):
        draw_centered_text(surface, "PLAYER 1", self.game.menu_font, self.game.player.color, 160, 40)
        draw_centered_text(surface, "PLAYER 2", self.game.menu_font, self.game.player2.color, WIDTH - 140, 40)

        if self.game.game_start_time:
            elapsed = (pygame.time.get_ticks() - self.game.game_start_time) // 1000
            minutes = elapsed // 60
            seconds = elapsed % 60
            time_text = f"{minutes:02}:{seconds:02}"
            draw_centered_text(surface, time_text, self.game.menu_font, WHITE, WIDTH // 2, 40)

        score_text = f"{self.game.score_p1} - {self.game.score_p2}"
        draw_centered_text(surface, score_text, self.game.menu_font, WHITE, WIDTH // 2, 70)

        self.game.player.draw(surface)
        self.game.player2.draw(surface)
