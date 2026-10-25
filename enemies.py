"""Marine creatures that can be extended with more enemy classes later."""

import math
import random

import pygame

from art import load_sprite, rotated_sprite, scaled_sprite
from camera import Camera
from region_data import normalize_region_id
import settings


class Jellyfish:
    def __init__(
        self,
        x: float,
        y: float,
        phase: float = 0.0,
        speed: float = 1.0,
        world_bounds: tuple[int, int, int, int] | None = None,
        region_id: str = "gulf",
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
        self.turn_rate = self.random.uniform(-0.45, 0.45)
        self.region_id = normalize_region_id(region_id)
        if self.region_id == "gulf":
            sprite = load_sprite("animals", "moon_jellyfish")
            size = (50, 71)
        elif self.region_id == "mediterranean":
            sprite = load_sprite("animals", "mediterranean_moon_jellyfish")
            size = (50, 71)
        else:
            hazard_art = {
                "arctic": ("animals", "lions_mane", (50, 71)),
                "great_lakes": ("animals", "sea_lamprey", (72, 38)),
                "amazon": ("animals", "stingray", (58, 48)),
            }
            category, name, size = hazard_art[self.region_id]
            sprite = load_sprite(f"regions/{self.region_id}/{category}", name)
        self.sprite = scaled_sprite(sprite, size)

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x - 21), round(self.y - 21), 42, 46)

    def update(self, dt: float) -> None:
        self.time += dt * self.speed
        self.wander_timer -= dt
        if self.wander_timer <= 0:
            self.turn_rate = self.random.uniform(-0.45, 0.45)
            self.wander_timer = self.random.uniform(1.0, 2.4)
            self.wander_speed = self.random.uniform(0.55, 1.15)
        self.heading += self.turn_rate * dt
        travel = 42 * self.speed * self.wander_speed * dt
        self.x += math.cos(self.heading) * travel
        self.y += math.sin(self.heading) * travel

        if self.world_bounds is not None:
            left, top, right, bottom = self.world_bounds
        else:
            left, top, right, bottom = (
                35,
                settings.HUD_HEIGHT + 50,
                settings.WORLD_WIDTH - 35,
                settings.WORLD_HEIGHT - 48,
            )
        if self.x < left + 45 or self.x > right - 45:
            self.heading = math.pi - self.heading
        if self.y < top + 50 or self.y > bottom - 50:
            self.heading = -self.heading
        self.x = max(left + 45, min(right - 45, self.x))
        self.y = max(top + 50, min(bottom - 50, self.y))

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
        region_id: str = "gulf",
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
        normalized_region = normalize_region_id(region_id)
        if normalized_region == "gulf":
            hunter_sprite = load_sprite("animals", "bull_shark")
        elif normalized_region == "mediterranean":
            hunter_sprite = load_sprite("animals", "mediterranean_barracuda")
        else:
            hunter_sprite = load_sprite(
                f"regions/{normalized_region}/animals",
                {
                    "arctic": "greenland_shark",
                    "great_lakes": "muskellunge",
                    "amazon": "black_caiman",
                }[normalized_region],
            )
        art = scaled_sprite(hunter_sprite, (96, 58))
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
