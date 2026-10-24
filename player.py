"""Player movement, health, and simple diver artwork."""

import math

import pygame

from art import load_sprite, rotated_sprite, scaled_sprite
from camera import Camera
import settings


class Player:
    def __init__(
        self,
        world_bounds: tuple[float, float, float, float] | None = None,
        start_position: tuple[float, float] = (500.0, 480.0),
    ) -> None:
        diver_art = scaled_sprite(load_sprite("player", "diver"), (84, 58))
        self.sprite_right = diver_art
        self.sprite_left = pygame.transform.flip(diver_art, True, False)
        self.bubble_sprite = load_sprite("effects", "bubble")
        self.swim_vertical = 0.0
        self.bubble_timer = 0.0
        self.bubbles: list[list[float]] = []
        self.radius = settings.PLAYER_RADIUS
        self.world_bounds = world_bounds or (
            0.0,
            0.0,
            float(settings.WORLD_WIDTH),
            float(settings.WORLD_HEIGHT),
        )
        self.start_position = start_position
        self.reset()

    def reset(self) -> None:
        self.x, self.y = self.start_position
        self.health = settings.PLAYER_STARTING_HEALTH
        self.invulnerability_timer = 0.0
        self.animation_time = 0.0
        self.facing = 1
        self.boosting = False
        self.swim_vertical = 0.0
        self.bubble_timer = 0.0
        self.bubbles.clear()

    @property
    def rect(self) -> pygame.Rect:
        """A slightly forgiving rectangle used for simple collisions."""
        size = self.radius * 1.5
        return pygame.Rect(round(self.x - size / 2), round(self.y - size / 2), size, size)

    def update(self, dt: float, keys: pygame.key.ScancodeWrapper) -> None:
        dx = float(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - float(
            keys[pygame.K_a] or keys[pygame.K_LEFT]
        )
        dy = float(keys[pygame.K_s] or keys[pygame.K_DOWN]) - float(
            keys[pygame.K_w] or keys[pygame.K_UP]
        )

        length = math.hypot(dx, dy)
        if length:
            dx /= length
            dy /= length
            self.facing = 1 if dx >= 0 else -1
        self.swim_vertical += (dy - self.swim_vertical) * min(1.0, dt * 5.0)

        self.boosting = bool(keys[pygame.K_SPACE])
        speed = settings.PLAYER_SPEED
        if self.boosting:
            speed *= settings.PLAYER_BOOST_MULTIPLIER

        self.x += dx * speed * dt
        self.y += dy * speed * dt
        left, top, right, bottom = self.world_bounds
        self.x = max(left + self.radius + 8, min(right - self.radius - 8, self.x))
        self.y = max(top + self.radius + 8, min(bottom - self.radius - 12, self.y))
        self.animation_time += dt * (1.8 if length else 0.7)
        self.invulnerability_timer = max(0.0, self.invulnerability_timer - dt)

        interval = 0.12 if self.boosting else 0.28
        if length:
            self.bubble_timer += dt
            while self.bubble_timer >= interval:
                self.bubble_timer -= interval
                self.bubbles.append(
                    [self.x - self.facing * 20, self.y + 4, 0.75, self.animation_time]
                )
        else:
            self.bubble_timer = 0.0

        for bubble in self.bubbles:
            bubble[1] -= 25 * dt
            bubble[0] += math.sin(bubble[3] + self.animation_time) * 7 * dt
            bubble[2] -= dt
        self.bubbles = [bubble for bubble in self.bubbles if bubble[2] > 0]

    def take_damage(self) -> bool:
        """Lose one heart unless the player is still invulnerable."""
        if self.invulnerability_timer > 0 or self.health <= 0:
            return False
        self.health -= 1
        self.invulnerability_timer = settings.PLAYER_INVULNERABILITY_SECONDS
        return True

    def draw(self, screen: pygame.Surface, camera: Camera) -> None:
        # Blink during the short post-hit invulnerability period.
        if self.invulnerability_timer > 0 and int(self.invulnerability_timer * 12) % 2 == 0:
            return

        bob = math.sin(self.animation_time * 4) * 2.5
        x, y = camera.world_to_screen((self.x, self.y + bob))
        image = self.sprite_left if self.facing < 0 else self.sprite_right
        image = rotated_sprite(image, -self.swim_vertical * 7)
        screen.blit(image, image.get_rect(center=(x, y)))

        for bubble_x, bubble_y, life, _phase in self.bubbles:
            radius = 10 if life > 0.4 else 7
            bubble = scaled_sprite(self.bubble_sprite, (radius, radius))
            bubble_position = camera.world_to_screen((bubble_x, bubble_y))
            screen.blit(bubble, bubble.get_rect(center=bubble_position))

        if self.boosting:
            puff_x = x - self.facing * 39
            pygame.draw.circle(screen, (121, 227, 238), (puff_x, y), 5)
            pygame.draw.circle(screen, (186, 246, 244), (puff_x - self.facing * 8, y - 5), 3)
