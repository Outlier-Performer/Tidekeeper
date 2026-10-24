"""Animated, asset-free underwater scenery."""

import math
import random

import pygame

import settings


class Ocean:
    def __init__(self) -> None:
        self.time = 0.0
        self.reef_health = 0.0
        self.random = random.Random(18)
        self.bubbles = [
            [self.random.randrange(settings.WIDTH), self.random.randrange(settings.HEIGHT), self.random.uniform(14, 42)]
            for _ in range(34)
        ]
        self.seaweed = [
            (x, self.random.randrange(settings.OCEAN_FLOOR_Y - 80, settings.OCEAN_FLOOR_Y + 3), self.random.randrange(42, 105))
            for x in range(18, settings.WIDTH, 48)
        ]
        self.coral_positions = [
            (95, settings.OCEAN_FLOOR_Y - 12, 0),
            (255, settings.OCEAN_FLOOR_Y - 8, 1),
            (500, settings.OCEAN_FLOOR_Y - 11, 2),
            (745, settings.OCEAN_FLOOR_Y - 10, 0),
            (910, settings.OCEAN_FLOOR_Y - 14, 1),
        ]
        self.gradient = self._make_gradient()
        self.clarity_overlay = pygame.Surface((settings.WIDTH, settings.OCEAN_FLOOR_Y))
        self.clarity_overlay.fill((91, 215, 197))

    def _make_gradient(self) -> pygame.Surface:
        surface = pygame.Surface((settings.WIDTH, settings.HEIGHT))
        top = (7, 53, 91)
        bottom = (18, 130, 151)
        for y in range(settings.HEIGHT):
            amount = y / settings.HEIGHT
            color = tuple(round(top[i] + (bottom[i] - top[i]) * amount) for i in range(3))
            pygame.draw.line(surface, color, (0, y), (settings.WIDTH, y))
        return surface

    def set_reef_health(self, health: float) -> None:
        self.reef_health = max(0.0, min(1.0, health))

    def update(self, dt: float) -> None:
        self.time += dt
        for bubble in self.bubbles:
            bubble[1] -= bubble[2] * dt
            bubble[0] += math.sin(self.time * 1.7 + bubble[1] * 0.025) * 7 * dt
            if bubble[1] < settings.HUD_HEIGHT:
                bubble[1] = settings.HEIGHT + self.random.randrange(10, 180)
                bubble[0] = self.random.randrange(settings.WIDTH)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.gradient, (0, 0))
        self.clarity_overlay.set_alpha(round(54 * self.reef_health))
        screen.blit(self.clarity_overlay, (0, 0))
        self._draw_light_rays(screen)
        self._draw_bubbles(screen)
        self._draw_seafloor(screen)
        self._draw_seaweed(screen)
        self._draw_coral(screen)

    def _draw_light_rays(self, screen: pygame.Surface) -> None:
        layer = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)
        clarity = self.reef_health
        for index in range(5):
            x = int(85 + index * 215 + math.sin(self.time * 0.22 + index) * 34)
            width = 46 + int(clarity * 24)
            pygame.draw.polygon(
                layer,
                (123, 231, 224, 13 + int(clarity * 12)),
                [(x, 0), (x + width, 0), (x + width * 3, settings.OCEAN_FLOOR_Y), (x - width, settings.OCEAN_FLOOR_Y)],
            )
        screen.blit(layer, (0, 0))

    def _draw_bubbles(self, screen: pygame.Surface) -> None:
        for x, y, speed in self.bubbles:
            radius = 2 + int(speed / 18)
            pygame.draw.circle(screen, (156, 232, 231), (int(x), int(y)), radius, 1)
            pygame.draw.circle(screen, (218, 255, 249), (int(x - 1), int(y - 1)), 1)

    def _draw_seafloor(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, (20, 81, 91), (0, settings.OCEAN_FLOOR_Y, settings.WIDTH, settings.HEIGHT - settings.OCEAN_FLOOR_Y))
        pygame.draw.ellipse(screen, (33, 102, 104), (-80, settings.OCEAN_FLOOR_Y - 18, 430, 62))
        pygame.draw.ellipse(screen, (28, 91, 100), (370, settings.OCEAN_FLOOR_Y - 12, 390, 54))
        pygame.draw.ellipse(screen, (37, 111, 105), (720, settings.OCEAN_FLOOR_Y - 19, 430, 65))

    def _draw_seaweed(self, screen: pygame.Surface) -> None:
        for index, (x, base_y, height) in enumerate(self.seaweed):
            sway = math.sin(self.time * 1.5 + index * 0.7) * 12
            color = tuple(int(channel * (0.82 + self.reef_health * 0.18)) for channel in settings.SEAWEED_GREEN)
            points = [
                (x, base_y),
                (int(x + sway * 0.45), base_y - height // 3),
                (int(x - sway * 0.35), base_y - height * 2 // 3),
                (int(x + sway), base_y - height),
            ]
            pygame.draw.lines(screen, color, False, points, 5)
            for px, py in points[1:]:
                pygame.draw.ellipse(screen, color, (px - 6, py - 10, 12, 20))

    def _draw_coral(self, screen: pygame.Surface) -> None:
        fade = self.reef_health
        palette = [settings.CORAL_PINK, settings.CORAL_ORANGE, settings.CORAL_PURPLE]
        for x, base_y, palette_index in self.coral_positions:
            muted = (109, 114, 111)
            target = palette[palette_index]
            color = tuple(round(muted[i] + (target[i] - muted[i]) * fade) for i in range(3))
            sway = math.sin(self.time * 1.2 + x) * 3
            pygame.draw.line(screen, color, (x, base_y), (int(x + sway), base_y - 49), 8)
            pygame.draw.line(screen, color, (x, base_y - 20), (x - 24, base_y - 43), 6)
            pygame.draw.line(screen, color, (x - 24, base_y - 43), (x - 29, base_y - 57), 5)
            pygame.draw.line(screen, color, (x, base_y - 29), (x + 23, base_y - 48), 6)
            pygame.draw.line(screen, color, (x + 23, base_y - 48), (x + 29, base_y - 62), 5)
            pygame.draw.circle(screen, color, (int(x + sway), base_y - 49), 5)
            pygame.draw.circle(screen, color, (x - 29, base_y - 57), 4)
            pygame.draw.circle(screen, color, (x + 29, base_y - 62), 4)
