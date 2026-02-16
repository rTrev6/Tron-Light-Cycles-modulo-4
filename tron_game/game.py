import pygame
import random
from arcade_machine_sdk import GameBase, GameMeta
from tron_game.player import Player
from tron_game.ui import *
from tron_game.settings import *
from tron_game.fonts import *

from tron_game.state_manager import StateManager
from tron_game.state_definitions import State
from tron_game.states.menu_state import MenuState
from tron_game.states.countdown_state import CountdownState
from tron_game.states.game_state import GameState
from tron_game.states.pause_state import PauseState
from tron_game.states.game_over_state import GameOverState

class TronGame(GameBase):
    def __init__(self, metadata: GameMeta):
        super().__init__(metadata)
        self.title_font = get_title_font(60)
        self.menu_font = get_menu_font(30)
        self.go_font = get_game_over_font(70)
        self.countdown_font = get_title_font(60)
        self.title_anim = ColorCycler(interval=600)

        self.score_p1 = 0
        self.score_p2 = 0
        self.winner = ""

        self.player = Player(STEP * 3, HEIGHT // 2, CYAN, CONTROLS_P1)
        self.player2 = Player(WIDTH - STEP * 4, HEIGHT // 2, ORANGE, CONTROLS_P2)

        self.state_manager = StateManager(self)
        self.state_manager.register(State.MENU, MenuState(self))
        self.state_manager.register(State.COUNTDOWN, CountdownState(self))
        self.state_manager.register(State.GAME, GameState(self))
        self.state_manager.register(State.PAUSE, PauseState(self))
        self.state_manager.register(State.GAME_OVER, GameOverState(self))
        self.state_manager.change(State.MENU)

    def handle_events(self, events):
        self.state_manager.handle_events(events)

    def update(self, dt):
        self.state_manager.update(dt)

    def render(self):
        surface = self.surface
        surface.fill(BLACK)
        self.state_manager.render(surface)

    def reset_game(self):
        colors = random.sample(COLORS_VAR, 2)
        self.player = Player(STEP * 3, HEIGHT // 2, colors[0], CONTROLS_P1)
        self.player2 = Player(WIDTH - STEP * 4, HEIGHT // 2, colors[1], CONTROLS_P2)
        self.player.direction = None
        self.player2.direction = None
        self.winner = ""
        self.game_start_time = None

    def reset_all(self):
        self.score_p1 = 0
        self.score_p2 = 0
        self.reset_game()
