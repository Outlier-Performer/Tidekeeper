"""Marine creatures that can be extended with more enemy classes later."""

import math

import pygame

from art import load_sprite, rotated_sprite, scaled_sprite
from camera import Camera
import settings


class Jellyfish:
    def __init__(self, x: float, y: float, phase: float = 0.0, speed: float = 1.0) -> None:
        self.x = x
        self.y = y
        self.anchor_x = x
        self.anchor_y = y
        self.phase = phase
        self.speed = speed
        self.time = 0.0
        self.sprite = scaled_sprite(load_sprite("animals", "moon_jellyfish"), (54, 57))

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x - 21), round(self.y - 21), 42, 46)

    def update(self, dt: float) -> None:
        self.time += dt * self.speed
        self.x = self.anchor_x + math.sin(self.time * 0.85 + self.phase) * 105
        self.y = self.anchor_y + math.sin(self.time * 1.45 + self.phase) * 48
        self.x = max(35, min(settings.WORLD_WIDTH - 35, self.x))
        self.y = max(settings.HUD_HEIGHT + 50, min(settings.WORLD_HEIGHT - 48, self.y))

    def draw(self, screen: pygame.Surface, camera: Camera) -> None:
        if not camera.sees((self.x, self.y), 60):
            return
        x, y = camera.world_to_screen((self.x, self.y))
        image = rotated_sprite(self.sprite, math.sin(self.time * 2.4 + self.phase) * 7)
        screen.blit(image, image.get_rect(center=(x, y)))


class Shark:
    """A simple shark chaser used in the compact cleanup game."""

    def __init__(self, x: float, y: float, speed: float = 85.0) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.facing = -1
        self.time = 0.0
        art = scaled_sprite(load_sprite("animals", "bull_shark"), (96, 58))
        self.sprite_right = art
        self.sprite_left = pygame.transform.flip(art, True, False)

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x - 43), round(self.y - 27), 86, 54)

    def update(self, dt: float, target: tuple[float, float]) -> None:
        self.time += dt
        dx = target[0] - self.x
        dy = target[1] - self.y
        distance = math.hypot(dx, dy)
        if distance > 1:
            self.x += dx / distance * self.speed * dt
            self.y += dy / distance * self.speed * dt
            if abs(dx) > 2:
                self.facing = 1 if dx > 0 else -1

    def draw(self, screen: pygame.Surface, camera: Camera) -> None:
        if not camera.sees((self.x, self.y), 55):
            return
        x, y = camera.world_to_screen((self.x, self.y))
        image = self.sprite_right if self.facing > 0 else self.sprite_left
        screen.blit(image, image.get_rect(center=(x, y)))
