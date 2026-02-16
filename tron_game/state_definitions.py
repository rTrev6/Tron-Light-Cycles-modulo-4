from enum import Enum

class State(Enum):
    MENU = "MENU"
    COUNTDOWN = "COUNTDOWN"
    GAME = "GAME"
    PAUSE = "PAUSE"
    GAME_OVER = "GAME_OVER"
