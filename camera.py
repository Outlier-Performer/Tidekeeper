"""Follow the player and convert world positions into screen positions."""

import pygame

import settings


class Camera:
    def __init__(self) -> None:
        self.x = 0.0
        self.y = 0.0

    def update(self, target: tuple[float, float], dt: float) -> None:
        """Smoothly center on a world position while respecting world edges."""
        desired_x = target[0] - settings.WIDTH / 2
        desired_y = target[1] - settings.HEIGHT / 2
        follow = min(1.0, settings.CAMERA_FOLLOW_SPEED * dt)
        self.x += (desired_x - self.x) * follow
        self.y += (desired_y - self.y) * follow
        self.x = max(0.0, min(settings.WORLD_WIDTH - settings.WIDTH, self.x))
        self.y = max(0.0, min(settings.WORLD_HEIGHT - settings.HEIGHT, self.y))

    def world_to_screen(self, position: tuple[float, float]) -> tuple[int, int]:
        return round(position[0] - self.x), round(position[1] - self.y)

    def screen_to_world(self, position: tuple[int, int]) -> tuple[float, float]:
        return position[0] + self.x, position[1] + self.y

    def rect_to_screen(self, rect: pygame.Rect) -> pygame.Rect:
        return rect.move(-round(self.x), -round(self.y))

    def sees(self, position: tuple[float, float], margin: int = 0) -> bool:
        return (
            self.x - margin <= position[0] <= self.x + settings.WIDTH + margin
            and self.y - margin <= position[1] <= self.y + settings.HEIGHT + margin
        )
