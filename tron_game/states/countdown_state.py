import pygame
from tron_game.state_definitions import State
from tron_game.ui import draw_centered_text
from tron_game.settings import WIDTH, HEIGHT, WHITE

class CountdownState:
    def __init__(self, game, arcade_mode = False):
        self.game = game
        self.arcade_mode = arcade_mode
        self.start_time = None
        self.duration = 1500  # milisegundos

    def enter(self):
        self.start_time = pygame.time.get_ticks()

    def handle_events(self, events):
        pass

    def update(self, dt):
        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed >= self.duration:
            self.game.player.direction = "right"
            self.game.player2.direction = "left"
            self.game.game_start_time = pygame.time.get_ticks()
            self.game.play_game_music() 
            self.game.state_manager.change(State.GAME, self.game, arcade_mode = self.arcade_mode)

    def render(self, surface):
        elapsed = pygame.time.get_ticks() - self.start_time
        remaining = 3 - (elapsed // 500)
        text = str(remaining) if remaining > 0 else "¡GO!"
        draw_centered_text(surface, text, self.game.countdown_font, WHITE, WIDTH // 2, HEIGHT // 2)
