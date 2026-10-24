"""Floating pollution collectibles and their simple pickup effects."""

import math
import random

import pygame

from art import load_sprite, scaled_sprite
from camera import Camera
from region_data import REGION_POLLUTION_PROFILES, REGION_TINTS, normalize_region_id
import settings


class PollutionItem:
    def __init__(self, x: float, y: float, kind: str, region_id: str = "gulf") -> None:
        self.x = x
        self.base_y = y
        self.kind = kind
        self.region_id = normalize_region_id(region_id)
        self.phase = random.random() * math.tau
        self.age = 0.0
        self.radius = 16

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x - 15), round(self.y - 15), 30, 30)

    @property
    def y(self) -> float:
        return self.base_y + math.sin(self.age * 2.2 + self.phase) * 7

    def update(self, dt: float) -> None:
        self.age += dt

    def draw(self, screen: pygame.Surface, camera: Camera) -> None:
        if not camera.sees((self.x, self.y), 30):
            return
        x, y = camera.world_to_screen((self.x, self.y))
        if self.region_id == "mediterranean":
            sprite = scaled_sprite(
                load_sprite("pollution", f"mediterranean_{self.kind}"),
                (36, 36),
            )
            screen.blit(sprite, sprite.get_rect(center=(x, y)))
            pygame.draw.circle(screen, (255, 222, 190), (x + 12, y - 12), 3)
            return
        if self.region_id not in ("gulf", "mediterranean"):
            sprite = scaled_sprite(
                load_sprite(f"regions/{self.region_id}/pollution", self.kind),
                (38, 38),
            )
            screen.blit(sprite, sprite.get_rect(center=(x, y)))
            pygame.draw.circle(screen, (255, 240, 215), (x + 12, y - 12), 3)
            return

        if self.kind == "bottle":
            pygame.draw.rect(screen, (120, 224, 205), (x - 7, y - 12, 14, 25), border_radius=4)
            pygame.draw.rect(screen, (217, 255, 241), (x - 4, y - 16, 8, 6), border_radius=2)
            pygame.draw.rect(screen, (75, 169, 166), (x - 5, y - 2, 10, 2))
        elif self.kind == "can":
            pygame.draw.rect(screen, (203, 180, 115), (x - 9, y - 11, 18, 23), border_radius=5)
            pygame.draw.ellipse(screen, (236, 215, 157), (x - 9, y - 12, 18, 6))
            pygame.draw.ellipse(screen, (145, 132, 99), (x - 9, y + 6, 18, 6))
            pygame.draw.line(screen, (244, 234, 195), (x - 4, y - 6), (x + 4, y - 6), 2)
        else:
            pygame.draw.rect(screen, (207, 177, 113), (x - 13, y - 10, 26, 20), 2)
            for offset in (-8, 0, 8):
                pygame.draw.line(screen, (222, 202, 148), (x + offset, y - 9), (x + offset, y + 9), 1)
            for offset in (-5, 3):
                pygame.draw.line(screen, (222, 202, 148), (x - 12, y + offset), (x + 12, y + offset), 1)

        pygame.draw.circle(screen, settings.POLLUTION_YELLOW, (x + 12, y - 12), 3)


class PickupEffect:
    def __init__(self, x: float, y: float, region_id: str = "gulf") -> None:
        self.x = x
        self.y = y
        self.age = 0.0
        self.region_id = normalize_region_id(region_id)

    def update(self, dt: float) -> None:
        self.age += dt

    def draw(self, screen: pygame.Surface, camera: Camera) -> None:
        if not camera.sees((self.x, self.y), 40):
            return
        progress = min(1.0, self.age / 0.45)
        radius = round(7 + progress * 26)
        x, y = camera.world_to_screen((self.x, self.y))
        tint = REGION_TINTS[self.region_id]
        color = (
            (255, 160, 178)
            if self.region_id == "mediterranean"
            else (tint[:3] if tint is not None else (175, 255, 211))
        )
        pygame.draw.circle(screen, color, (x, y), radius, 2)


class PollutionField:
    def __init__(
        self,
        world_bounds: tuple[int, int, int, int] | None = None,
        spawn_new_items: bool = True,
        initial_item_count: int = 7,
        region_id: str = "gulf",
    ) -> None:
        self.random = random.Random()
        self.items: list[PollutionItem] = []
        self.effects: list[PickupEffect] = []
        self.spawn_timer = 0.0
        self.spawn_new_items = spawn_new_items
        self.initial_item_count = initial_item_count
        self.region_id = normalize_region_id(region_id)
        self.world_bounds = world_bounds or (
            0,
            settings.HUD_HEIGHT,
            settings.WORLD_WIDTH,
            settings.WORLD_HEIGHT,
        )
        self.reset()

    def reset(
        self,
        player_position: tuple[float, float] | None = (500.0, 480.0),
        item_count: int | None = None,
    ) -> None:
        self.items.clear()
        self.effects.clear()
        self.spawn_timer = 0.0
        for _ in range(self.initial_item_count if item_count is None else item_count):
            self._spawn_item(player_position)

    def _spawn_item(self, player_position: tuple[float, float] | None) -> None:
        left, top, right, bottom = self.world_bounds
        if player_position is None:
            x = self.random.randint(left + 42, right - 42)
            y = self.random.randint(top + 45, bottom - 55)
        else:
            x = round(player_position[0] + self.random.randint(-settings.ITEM_SPAWN_RADIUS_X, settings.ITEM_SPAWN_RADIUS_X))
            y = round(player_position[1] + self.random.randint(-settings.ITEM_SPAWN_RADIUS_Y, settings.ITEM_SPAWN_RADIUS_Y))
            x = max(left + 42, min(right - 42, x))
            y = max(top + 45, min(bottom - 55, y))
        pollution_kinds = tuple(REGION_POLLUTION_PROFILES[self.region_id])
        kind = self.random.choice(pollution_kinds)
        self.items.append(PollutionItem(x, y, kind, self.region_id))

    def update(self, dt: float, player_position: tuple[float, float]) -> None:
        if self.spawn_new_items:
            self.spawn_timer += dt
            while self.spawn_timer >= settings.ITEM_SPAWN_INTERVAL and len(self.items) < settings.MAX_POLLUTION_ITEMS:
                self.spawn_timer -= settings.ITEM_SPAWN_INTERVAL
                self._spawn_item(player_position)

        for item in self.items:
            item.update(dt)
        for effect in self.effects:
            effect.update(dt)
        self.effects = [effect for effect in self.effects if effect.age < 0.45]

    def collect_collisions(self, player_rect: pygame.Rect) -> list[tuple[int, int]]:
        """Remove touched items and return their pickup positions to the game."""
        collected: list[tuple[int, int]] = []
        remaining: list[PollutionItem] = []
        for item in self.items:
            if item.rect.colliderect(player_rect):
                position = (round(item.x), round(item.y))
                collected.append(position)
                self.effects.append(PickupEffect(*position, item.region_id))
            else:
                remaining.append(item)
        self.items = remaining
        return collected

    def draw(self, screen: pygame.Surface, camera: Camera) -> None:
        for item in self.items:
            item.draw(screen, camera)
        for effect in self.effects:
            effect.draw(screen, camera)
