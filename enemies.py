"""Marine creatures that can be extended with more enemy classes later."""

import math
import random

import pygame

from art import load_sprite, rotated_sprite, scaled_sprite
from camera import Camera
import settings


class Jellyfish:
    def __init__(
        self,
        x: float,
        y: float,
        phase: float = 0.0,
        speed: float = 1.0,
        world_bounds: tuple[int, int, int, int] | None = None,
    ) -> None:
        self.x = x
        self.y = y
        self.anchor_x = x
        self.anchor_y = y
        self.phase = phase
        self.speed = speed
        self.time = 0.0
        self.world_bounds = world_bounds
        self.random = random.Random()
        self.heading = self.random.uniform(0, math.tau)
        self.wander_timer = self.random.uniform(0.2, 1.0)
        self.wander_speed = self.random.uniform(0.65, 1.35)
        self.sprite = scaled_sprite(load_sprite("animals", "moon_jellyfish"), (50, 71))

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x - 21), round(self.y - 21), 42, 46)

    def update(self, dt: float) -> None:
        self.time += dt * self.speed
        if self.world_bounds is not None:
            left, top, right, bottom = self.world_bounds
            self.wander_timer -= dt
            if self.wander_timer <= 0:
                self.heading += self.random.uniform(-math.pi, math.pi)
                self.wander_timer = self.random.uniform(0.45, 2.0)
                self.wander_speed = self.random.uniform(0.55, 1.45)
            travel = 42 * self.speed * self.wander_speed * dt
            self.x += math.cos(self.heading) * travel
            self.y += math.sin(self.heading) * travel
            if self.x < left + 45 or self.x > right - 45:
                self.heading = math.pi - self.heading
            if self.y < top + 50 or self.y > bottom - 50:
                self.heading = -self.heading
            self.x = max(left + 45, min(right - 45, self.x))
            self.y = max(top + 50, min(bottom - 50, self.y))
            return

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

    def __init__(
        self,
        x: float,
        y: float,
        speed: float = 85.0,
        world_bounds: tuple[int, int, int, int] | None = None,
        tracking_distance: float = 420.0,
    ) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.tracking_distance = tracking_distance
        self.world_bounds = world_bounds or (
            0,
            settings.HUD_HEIGHT,
            settings.WORLD_WIDTH,
            settings.WORLD_HEIGHT,
        )
        self.facing = -1
        self.time = 0.0
        self.random = random.Random()
        self.wander_target = self._random_wander_target()
        art = scaled_sprite(load_sprite("animals", "bull_shark"), (96, 58))
        self.sprite_right = art
        self.sprite_left = pygame.transform.flip(art, True, False)

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x - 43), round(self.y - 27), 86, 54)

    def update(self, dt: float, target: tuple[float, float]) -> None:
        self.time += dt
        distance_to_player = math.hypot(target[0] - self.x, target[1] - self.y)
        if distance_to_player <= self.tracking_distance:
            destination = target
        else:
            dx = self.wander_target[0] - self.x
            dy = self.wander_target[1] - self.y
            if math.hypot(dx, dy) < 25:
                self.wander_target = self._random_wander_target()
            destination = self.wander_target

        dx = destination[0] - self.x
        dy = destination[1] - self.y
        distance = math.hypot(dx, dy)
        if distance > 1:
            movement_speed = (
                self.speed
                if distance_to_player <= self.tracking_distance
                else self.speed * 0.7
            )
            self.x += dx / distance * movement_speed * dt
            self.y += dy / distance * movement_speed * dt
            if abs(dx) > 2:
                self.facing = 1 if dx > 0 else -1
        left, top, right, bottom = self.world_bounds
        self.x = max(left + 45, min(right - 45, self.x))
        self.y = max(top + 30, min(bottom - 30, self.y))

    def _random_wander_target(self) -> tuple[float, float]:
        left, top, right, bottom = self.world_bounds
        return (
            self.random.uniform(left + 50, right - 50),
            self.random.uniform(top + 35, bottom - 35),
        )

    def draw(self, screen: pygame.Surface, camera: Camera) -> None:
        if not camera.sees((self.x, self.y), 55):
            return
        x, y = camera.world_to_screen((self.x, self.y))
        image = self.sprite_right if self.facing > 0 else self.sprite_left
        image = rotated_sprite(image, math.sin(self.time * 5.5) * 2.0)
        screen.blit(image, image.get_rect(center=(x, y)))
