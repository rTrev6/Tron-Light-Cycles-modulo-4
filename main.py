from tron_game.game import TronGame
from arcade_machine_sdk import GameMeta
import pygame

if not pygame.get_init():
    pygame.init()

metadata = (
    GameMeta()
    .with_title("Tron Light Cycles")
    .with_description("Juego de motos de luz estilo TRON para dos jugadores")
    .with_release_date("2026-02-15")
    .with_group_number(3)
    .add_author("Rickz")
    .add_tag("Arcade")
    .add_tag("Multijugador")
)

game = TronGame(metadata)

if __name__ == "__main__":
    game.run_independently()
