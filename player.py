"""Player movement, health, and simple diver artwork."""

import math

import pygame

import settings


class Player:
    def __init__(self) -> None:
        self.radius = settings.PLAYER_RADIUS
        self.reset()

    def reset(self) -> None:
        self.x = settings.WIDTH * 0.5
        self.y = settings.HEIGHT * 0.55
        self.health = settings.PLAYER_STARTING_HEALTH
        self.invulnerability_timer = 0.0
        self.animation_time = 0.0
        self.facing = 1
        self.boosting = False

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

        self.boosting = bool(keys[pygame.K_SPACE])
        speed = settings.PLAYER_SPEED
        if self.boosting:
            speed *= settings.PLAYER_BOOST_MULTIPLIER

        self.x += dx * speed * dt
        self.y += dy * speed * dt
        self.x = max(self.radius + 8, min(settings.WIDTH - self.radius - 8, self.x))
        self.y = max(settings.HUD_HEIGHT + self.radius, min(settings.HEIGHT - self.radius - 12, self.y))
        self.animation_time += dt * (1.8 if length else 0.7)
        self.invulnerability_timer = max(0.0, self.invulnerability_timer - dt)

    def take_damage(self) -> bool:
        """Lose one heart unless the player is still invulnerable."""
        if self.invulnerability_timer > 0 or self.health <= 0:
            return False
        self.health -= 1
        self.invulnerability_timer = settings.PLAYER_INVULNERABILITY_SECONDS
        return True

    def draw(self, screen: pygame.Surface) -> None:
        # Blink during the short post-hit invulnerability period.
        if self.invulnerability_timer > 0 and int(self.invulnerability_timer * 12) % 2 == 0:
            return

        bob = math.sin(self.animation_time * 4) * 2.5
        x, y = round(self.x), round(self.y + bob)

        # Fins and tank
        tail_x = x - self.facing * 20
        pygame.draw.ellipse(screen, (248, 126, 109), (tail_x - 8, y - 5, 17, 11))
        pygame.draw.rect(screen, (171, 228, 228), (x - 3, y - 15, 10, 30), border_radius=5)

        # Suit, visor, and highlights
        pygame.draw.ellipse(screen, (255, 174, 100), (x - 17, y - 14, 35, 28))
        pygame.draw.circle(screen, (37, 81, 112), (x + self.facing * 5, y), 10)
        pygame.draw.circle(screen, (126, 225, 231), (x + self.facing * 7, y - 2), 7)
        pygame.draw.circle(screen, settings.WHITE, (x + self.facing * 9, y - 5), 2)
        pygame.draw.line(screen, (255, 225, 168), (x + self.facing * 15, y + 7), (x + self.facing * 22, y + 11), 3)

        if self.boosting:
            puff_x = x - self.facing * 27
            pygame.draw.circle(screen, (121, 227, 238), (puff_x, y), 5)
            pygame.draw.circle(screen, (186, 246, 244), (puff_x - self.facing * 8, y - 5), 3)
