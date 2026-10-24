"""Marine creatures that can be extended with more enemy classes later."""

import math

import pygame

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

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x - 20), round(self.y - 17), 40, 42)

    def update(self, dt: float) -> None:
        self.time += dt * self.speed
        self.x = self.anchor_x + math.sin(self.time * 0.85 + self.phase) * 105
        self.y = self.anchor_y + math.sin(self.time * 1.45 + self.phase) * 48
        self.x = max(35, min(settings.WIDTH - 35, self.x))
        self.y = max(settings.HUD_HEIGHT + 50, min(settings.OCEAN_FLOOR_Y - 48, self.y))

    def draw(self, screen: pygame.Surface) -> None:
        x, y = round(self.x), round(self.y)
        pulse = math.sin(self.time * 4 + self.phase) * 2
        width = round(42 + pulse)
        body = (242, 137, 190)
        pygame.draw.ellipse(screen, (255, 183, 216), (x - width // 2, y - 19, width, 31))
        pygame.draw.rect(screen, body, (x - width // 2, y - 3, width, 12), border_radius=5)
        for offset in (-13, 0, 13):
            wave = math.sin(self.time * 4 + offset + self.phase) * 4
            pygame.draw.line(screen, body, (x + offset, y + 7), (int(x + offset + wave), y + 25), 3)
            pygame.draw.line(screen, (255, 183, 216), (int(x + offset + wave), y + 25), (int(x + offset - wave), y + 35), 2)
        pygame.draw.circle(screen, (67, 66, 111), (x - 7, y - 2), 2)
        pygame.draw.circle(screen, (67, 66, 111), (x + 7, y - 2), 2)
