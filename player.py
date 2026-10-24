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
        self.swimming = False
        self.swim_phase = 0.0
        self.move_dx = 0.0
        self.move_dy = 0.0
        self.boost_energy = 1.0
        self.boost_recharge_timer = 0.0
        self.bubble_timer = 0.0
        self.bubbles.clear()

    @property
    def rect(self) -> pygame.Rect:
        """A slightly forgiving rectangle used for simple collisions."""
        size = self.radius * 1.5
        return pygame.Rect(round(self.x - size / 2), round(self.y - size / 2), size, size)

    def update(self, dt: float, keys: pygame.key.ScancodeWrapper) -> None:
        direction = pygame.Vector2(
            int(bool(keys[pygame.K_d] or keys[pygame.K_RIGHT]))
            - int(bool(keys[pygame.K_a] or keys[pygame.K_LEFT])),
            int(bool(keys[pygame.K_s] or keys[pygame.K_DOWN]))
            - int(bool(keys[pygame.K_w] or keys[pygame.K_UP])),
        )
        self.swimming = direction.length_squared() > 0
        if self.swimming:
            direction.normalize_ip()
            self.move_dx, self.move_dy = direction
            if direction.x != 0:
                self.facing = 1 if direction.x > 0 else -1
        else:
            self.move_dx = 0.0
            self.move_dy = 0.0
        self.swim_vertical += (self.move_dy - self.swim_vertical) * min(1.0, dt * 5.0)

        boost_requested = bool(keys[pygame.K_SPACE])
        self.boosting = boost_requested and self.boost_energy > 0 and self.swimming
        if self.boosting:
            self.boost_energy = max(
                0.0,
                self.boost_energy - dt / settings.PLAYER_BOOST_DRAIN_SECONDS,
            )
            self.boost_recharge_timer = settings.PLAYER_BOOST_RECHARGE_DELAY
        elif not boost_requested:
            self.boost_recharge_timer = max(0.0, self.boost_recharge_timer - dt)
            if self.boost_recharge_timer == 0:
                self.boost_energy = min(
                    1.0,
                    self.boost_energy + dt / settings.PLAYER_BOOST_RECHARGE_SECONDS,
                )

        speed = settings.PLAYER_SPEED
        if self.boosting:
            speed *= settings.PLAYER_BOOST_MULTIPLIER

        self.x += self.move_dx * speed * dt
        self.y += self.move_dy * speed * dt
        left, top, right, bottom = self.world_bounds
        self.x = max(left + self.radius + 8, min(right - self.radius - 8, self.x))
        self.y = max(top + self.radius + 8, min(bottom - self.radius - 12, self.y))
        self.animation_time += dt * (1.8 if self.swimming else 0.7)
        self.swim_phase += dt * (9.0 if self.swimming else 2.2)
        self.invulnerability_timer = max(0.0, self.invulnerability_timer - dt)

        interval = 0.12 if self.boosting else 0.28
        if self.swimming:
            self.bubble_timer += dt
            while self.bubble_timer >= interval:
                self.bubble_timer -= interval
                self.bubbles.append(
                    [
                        self.x - self.move_dx * 20,
                        self.y - self.move_dy * 20,
                        0.75,
                        self.animation_time,
                    ]
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

        bob = (
            math.sin(self.swim_phase) * 3.2
            if self.swimming
            else math.sin(self.animation_time * 2.5) * 1.4
        )
        x, y = camera.world_to_screen((self.x, self.y + bob))
        image = self.sprite_left if self.facing < 0 else self.sprite_right
        kick = math.sin(self.swim_phase) * 2.5 if self.swimming else 0.0
        image = rotated_sprite(
            image,
            -self.swim_vertical * 7 * self.facing + kick,
        )
        screen.blit(image, image.get_rect(center=(x, y)))

        for bubble_x, bubble_y, life, _phase in self.bubbles:
            radius = 10 if life > 0.4 else 7
            bubble = scaled_sprite(self.bubble_sprite, (radius, radius))
            bubble_position = camera.world_to_screen((bubble_x, bubble_y))
            screen.blit(bubble, bubble.get_rect(center=bubble_position))

        if self.boosting:
            puff_x = round(x - self.move_dx * 39)
            puff_y = round(y - self.move_dy * 39)
            pygame.draw.circle(screen, (121, 227, 238), (puff_x, puff_y), 5)
            pygame.draw.circle(
                screen,
                (186, 246, 244),
                (round(puff_x - self.move_dx * 8), round(puff_y - self.move_dy * 8)),
                3,
            )
