# player.py
import pygame
from pygame import Rect
from settings import PLAYER_SIZE, PLAYER_START_X, GROUND_Y, GRAVITY, JUMP_VELOCITY


# ...existing code...

class Player:
    def __init__(self, x=PLAYER_START_X, y=None, sprite=None):
        self.size = PLAYER_SIZE
        self.x = x
        self.y = (GROUND_Y - self.size) if y is None else y
        self.vy = 0.0
        self.on_ground = True
        self.rect = Rect(self.x, self.y, self.size, self.size)
        self.sprite = sprite
        self.angle = 0.0  # rotation for cube feel
        self.alive = True

    def jump(self):
        if self.on_ground:
            self.vy = JUMP_VELOCITY
            self.on_ground = False

    def update(self):
        self.vy += GRAVITY
        self.y += self.vy
        if self.y >= GROUND_Y - self.size:
            self.y = GROUND_Y - self.size
            self.vy = 0
            self.on_ground = True
            self.angle = 0.0  # Snap straight when landing
        else:
            self.on_ground = False
            self.angle += 12  # Rotate while in air
        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, surface):
        if self.sprite:
            rotated = pygame.transform.rotate(self.sprite, self.angle)
            r = rotated.get_rect(center=self.rect.center)
            surface.blit(rotated, r.topleft)
        else:
            pygame.draw.rect(surface, (70, 200, 250), self.rect)
# ...existing code...