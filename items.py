"""Floating pollution collectibles and their simple pickup effects."""

import math
import random

import pygame

import settings


class PollutionItem:
    def __init__(self, x: float, y: float, kind: str) -> None:
        self.x = x
        self.base_y = y
        self.kind = kind
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

    def draw(self, screen: pygame.Surface) -> None:
        x, y = round(self.x), round(self.y)
        if self.kind == "bottle":
            pygame.draw.rect(screen, (120, 224, 205), (x - 7, y - 12, 14, 25), border_radius=4)
            pygame.draw.rect(screen, (217, 255, 241), (x - 4, y - 16, 8, 6), border_radius=2)
            pygame.draw.rect(screen, (75, 169, 166), (x - 5, y - 2, 10, 2))
        else:
            pygame.draw.rect(screen, (203, 180, 115), (x - 9, y - 11, 18, 23), border_radius=5)
            pygame.draw.ellipse(screen, (236, 215, 157), (x - 9, y - 12, 18, 6))
            pygame.draw.ellipse(screen, (145, 132, 99), (x - 9, y + 6, 18, 6))
            pygame.draw.line(screen, (244, 234, 195), (x - 4, y - 6), (x + 4, y - 6), 2)

        pygame.draw.circle(screen, settings.POLLUTION_YELLOW, (x + 12, y - 12), 3)


class PickupEffect:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.age = 0.0

    def update(self, dt: float) -> None:
        self.age += dt

    def draw(self, screen: pygame.Surface) -> None:
        progress = min(1.0, self.age / 0.45)
        radius = round(7 + progress * 26)
        pygame.draw.circle(screen, (175, 255, 211), (round(self.x), round(self.y)), radius, 2)


class PollutionField:
    def __init__(self) -> None:
        self.random = random.Random()
        self.items: list[PollutionItem] = []
        self.effects: list[PickupEffect] = []
        self.spawn_timer = 0.0
        self.reset()

    def reset(self) -> None:
        self.items.clear()
        self.effects.clear()
        self.spawn_timer = 0.0
        for _ in range(7):
            self._spawn_item()

    def _spawn_item(self) -> None:
        x = self.random.randint(42, settings.WIDTH - 42)
        y = self.random.randint(settings.HUD_HEIGHT + 45, settings.OCEAN_FLOOR_Y - 55)
        kind = self.random.choice(("bottle", "can"))
        self.items.append(PollutionItem(x, y, kind))

    def update(self, dt: float) -> None:
        self.spawn_timer += dt
        while self.spawn_timer >= settings.ITEM_SPAWN_INTERVAL and len(self.items) < settings.MAX_POLLUTION_ITEMS:
            self.spawn_timer -= settings.ITEM_SPAWN_INTERVAL
            self._spawn_item()

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
                self.effects.append(PickupEffect(*position))
            else:
                remaining.append(item)
        self.items = remaining
        return collected

    def draw(self, screen: pygame.Surface) -> None:
        for item in self.items:
            item.draw(screen)
        for effect in self.effects:
            effect.draw(screen)
