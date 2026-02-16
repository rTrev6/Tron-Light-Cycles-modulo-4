import pygame
from tron_game.settings import *

class Player:
    def __init__(self, x, y, color, controls):
        self.x = x
        self.y = y
        self.color = color
        self.direction = None
        self.trail = []
        self.controls = controls

    def handle_input(self, keys):
        up = self.controls["UP"]
        down = self.controls["DOWN"]
        left = self.controls["LEFT"]
        right = self.controls["RIGHT"]

        if keys[up] and self.direction != "DOWN":
            self.direction = "UP"
        elif keys[down] and self.direction != "UP":
            self.direction = "DOWN"
        elif keys[left] and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif keys[right] and self.direction != "LEFT":
            self.direction = "RIGHT"

    def move(self, dt):
        if self.direction == "UP":
            self.y -= SPEED * dt
        elif self.direction == "DOWN":
            self.y += SPEED * dt
        elif self.direction == "LEFT":
            self.x -= SPEED * dt
        elif self.direction == "RIGHT":
            self.x += SPEED * dt

        # Redondeamos solo para guardar en la estela
        head = (round(self.x / STEP) * STEP, round(self.y / STEP) * STEP)
        if not self.trail or head != self.trail[-1]:
            self.trail.append(head)


    def check_self_collision(self):
        head = round(self.x / STEP ) * STEP, round(self.y / STEP ) * STEP
        return head in self.trail[:-1]

    def out_of_bounds(self):
        return (
            self.x < 0 or
            self.x + STEP > WIDTH or
            self.y < 0 or
            self.y + STEP > HEIGHT
        )

    def draw(self, surface):
        for pos in self.trail:
            pygame.draw.rect(surface, self.color, (pos[0], pos[1], STEP, STEP))
