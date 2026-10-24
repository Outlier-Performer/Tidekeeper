"""Procedurally generated, scrolling underwater environment."""

import math
import random

import pygame

from art import load_sprite, rotated_sprite, scaled_sprite
from camera import Camera
import settings
from world import HabitatZone, ZONES, water_color_at, zone_at


class Ocean:
    def __init__(self) -> None:
        self.time = 0.0
        self.reef_health = 0.0
        self.random = random.Random(18)
        self.backdrop = load_sprite("backgrounds", "gulf_backdrop").copy()
        self.floor_tile = load_sprite("terrain", "sandy_floor_tile")
        self.plant_sprites = {
            "seagrass": load_sprite("plants", "seagrass"),
            "sargassum": load_sprite("plants", "sargassum"),
        }
        self.coral_sprites = {
            "branch": load_sprite("coral", "branching_coral"),
            "brain": load_sprite("coral", "brain_coral"),
            "fan": load_sprite("coral", "sea_fan"),
        }
        self.coral_variants = self._make_coral_variants()
        self.rock_sprites = {
            "limestone": load_sprite("terrain", "limestone_reef"),
            "sandstone": load_sprite("terrain", "sandstone_reef"),
        }
        self.fish_sprites = {
            "red_snapper": load_sprite("fish", "red_snapper"),
            "blue_tang": load_sprite("fish", "blue_tang"),
            "queen_angelfish": load_sprite("fish", "queen_angelfish"),
        }
        self.fish_left_sprites = {
            species: pygame.transform.flip(sprite, True, False)
            for species, sprite in self.fish_sprites.items()
        }
        self.bubbles = [
            [
                self.random.randrange(settings.WORLD_WIDTH),
                self.random.randrange(settings.WORLD_HEIGHT),
                self.random.uniform(13, 38),
                self.random.uniform(2, 5),
            ]
            for _ in range(90)
        ]
        self.seaweed = self._make_seaweed()
        self.coral = self._make_coral()
        self.rocks = self._make_rocks()
        self.fish = self._make_fish_schools()
        self.light_layer = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)

    def _make_coral_variants(self) -> dict[str, list[pygame.Surface]]:
        variants = {}
        for name, sprite in self.coral_sprites.items():
            variants[name] = []
            for step in range(11):
                amount = step / 10
                tint = tuple(round(188 + (255 - 188) * amount) for _ in range(3))
                variant = sprite.copy()
                variant.fill((*tint, 255), special_flags=pygame.BLEND_RGBA_MULT)
                variants[name].append(variant)
        return variants

    def _make_seaweed(self) -> list[tuple[float, float, int, float, str]]:
        placements = []
        meadows = (
            (230, 850, "seagrass"),
            (680, 875, "seagrass"),
            (1190, 1800, "sargassum"),
            (1580, 1975, "seagrass"),
            (1880, 1975, "sargassum"),
            (2480, 1980, "seagrass"),
            (2920, 1950, "sargassum"),
            (3440, 1900, "seagrass"),
            (3800, 1970, "sargassum"),
        )
        for center_x, base_y, kind in meadows:
            for _ in range(6):
                placements.append(
                    (
                        center_x + self.random.randint(-110, 110),
                        base_y + self.random.randint(-35, 25),
                        self.random.randint(58, 108),
                        self.random.random() * math.tau,
                        kind if self.random.random() < 0.82 else (
                            "sargassum" if kind == "seagrass" else "seagrass"
                        ),
                    )
                )
        return placements

    def _make_coral(self) -> list[tuple[float, float, str, int, int, float]]:
        placements = []
        reef_groups = (
            (820, 1690, 6),
            (1320, 1910, 7),
            (1880, 2020, 9),
            (2480, 2020, 9),
            (3260, 1910, 7),
            (3680, 2010, 6),
        )
        kinds = ("branch", "brain", "fan")
        for center_x, base_y, count in reef_groups:
            for index in range(count):
                kind = kinds[index % len(kinds)]
                scale = self.random.uniform(0.50, 0.87)
                if 1600 <= center_x <= 2800:
                    scale *= 1.08
                source = self.coral_sprites[kind]
                placements.append(
                    (
                        center_x + self.random.randint(-125, 125),
                        base_y + self.random.randint(-32, 20),
                        kind,
                        round(source.get_width() * scale),
                        round(source.get_height() * scale),
                        self.random.random() * math.tau,
                    )
                )
        return placements

    def _make_rocks(self) -> list[tuple[float, float, int, int, str, float]]:
        placements = []
        rock_sites = (
            (180, 890),
            (600, 925),
            (1100, 1740),
            (1850, 2050),
            (2480, 2050),
            (3160, 1900),
            (3670, 2010),
            (420, 2810),
            (1450, 2800),
            (2580, 2820),
            (3650, 2780),
        )
        for index, (center_x, base_y) in enumerate(rock_sites):
            for _ in range(3 if index in (3, 4) else 2):
                scale = self.random.uniform(0.50, 0.88)
                placements.append(
                    (
                        center_x + self.random.randint(-72, 72),
                        base_y + self.random.randint(-18, 20),
                        round(180 * scale),
                        round(116 * scale),
                        "limestone" if self.random.random() < 0.6 else "sandstone",
                        self.random.random() * 8 - 4,
                    )
                )
        return placements

    def _make_fish_schools(self) -> list[tuple[float, float, float, float, str, float, int]]:
        fish = []
        schools = (
            (240, 390, "queen_angelfish", 6),
            (720, 700, "blue_tang", 7),
            (1260, 1570, "red_snapper", 6),
            (1730, 1640, "queen_angelfish", 7),
            (2190, 1670, "blue_tang", 8),
            (2730, 1670, "red_snapper", 7),
            (3290, 1600, "blue_tang", 6),
            (3670, 2340, "red_snapper", 6),
        )
        for center_x, center_y, species, count in schools:
            speed = self.random.uniform(0.42, 0.72)
            school_phase = self.random.random() * math.tau
            for index in range(count):
                fish.append(
                    (
                        center_x + self.random.randint(-95, 95),
                        center_y + self.random.randint(-54, 54),
                        self.random.uniform(23, 57),
                        speed + self.random.uniform(-0.06, 0.06),
                        species,
                        school_phase + index * 0.24,
                        self.random.randrange(12, 21),
                    )
                )
        return fish

    def set_reef_health(self, health: float) -> None:
        self.reef_health = max(0.0, min(1.0, health))

    def update(self, dt: float, camera: Camera) -> None:
        self.time += dt
        for bubble in self.bubbles:
            if not camera.sees((bubble[0], bubble[1]), 100):
                continue
            bubble[1] -= bubble[2] * dt
            bubble[0] += math.sin(self.time * bubble[3] + bubble[1] * 0.01) * 9 * dt
            if bubble[1] < 0:
                bubble[1] = settings.WORLD_HEIGHT - self.random.randrange(20, 180)
                bubble[0] = self.random.randrange(settings.WORLD_WIDTH)

    def draw(self, screen: pygame.Surface, camera: Camera) -> None:
        self._draw_water(screen, camera)
        self._draw_backdrop(screen, camera)
        self._draw_light_rays(screen, camera)
        self._draw_surface(screen, camera)
        self._draw_floor(screen, camera)
        self._draw_rocks(screen, camera)
        self._draw_seaweed(screen, camera)
        self._draw_coral(screen, camera)
        self._draw_fish(screen, camera)
        self._draw_bubbles(screen, camera)

    def _draw_water(self, screen: pygame.Surface, camera: Camera) -> None:
        band_height = 12
        for top in range(0, settings.HEIGHT, band_height):
            world_y = camera.y + top + band_height / 2
            color = list(water_color_at(world_y))
            screen_shade = 1.0 - ((top / settings.HEIGHT) * 0.13)
            clarity = self.reef_health * 0.10
            color = [
                min(255, round(channel * screen_shade + (170 - channel) * clarity))
                for channel in color
            ]
            pygame.draw.rect(screen, color, (0, top, settings.WIDTH, band_height))

    def _draw_light_rays(self, screen: pygame.Surface, camera: Camera) -> None:
        self.light_layer.fill((0, 0, 0, 0))
        if camera.y > 1450:
            return
        light_strength = max(0.0, 1.0 - camera.y / 1600)
        alpha = round(12 * light_strength + self.reef_health * 8)
        for index in range(5):
            x = int(65 + index * 230 + math.sin(self.time * 0.2 + index) * 34)
            width = 25 + int(self.reef_health * 9)
            pygame.draw.polygon(
                self.light_layer,
                (149, 240, 225, alpha),
                [(x, 0), (x + width, 0), (x + width * 3, settings.HEIGHT), (x - width, settings.HEIGHT)],
            )
        screen.blit(self.light_layer, (0, 0))

    def _draw_backdrop(self, screen: pygame.Surface, camera: Camera) -> None:
        image_width = self.backdrop.get_width()
        offset = round(camera.x * 0.18) % image_width
        brightness = max(0.22, 1.0 - camera.y / settings.WORLD_HEIGHT * 0.72)
        self.backdrop.set_alpha(round(255 * brightness))
        x = -offset
        while x < settings.WIDTH:
            screen.blit(self.backdrop, (x, 0))
            x += image_width
        self.backdrop.set_alpha(None)

    def _draw_surface(self, screen: pygame.Surface, camera: Camera) -> None:
        if camera.y > 150:
            return
        surface_y = round(-camera.y + 8)
        pygame.draw.rect(screen, (98, 218, 207), (0, surface_y, settings.WIDTH, 6))
        for index in range(18):
            x = index * 61 + int(self.time * 12) % 61
            wave_y = surface_y + round(math.sin(index + self.time * 1.5) * 4)
            pygame.draw.arc(screen, (181, 250, 232), (x, wave_y - 4, 70, 13), 0.2, 2.8, 2)

    def _draw_floor(self, screen: pygame.Surface, camera: Camera) -> None:
        floor_y = settings.OCEAN_FLOOR_Y
        if camera.y + settings.HEIGHT < floor_y:
            return
        screen_y = round(floor_y - camera.y)
        image_width = self.floor_tile.get_width()
        x = -(round(camera.x) % image_width) - image_width
        while x < settings.WIDTH:
            y = screen_y
            while y < settings.HEIGHT:
                screen.blit(self.floor_tile, (x, y))
                y += self.floor_tile.get_height()
            x += image_width

    def _draw_rocks(self, screen: pygame.Surface, camera: Camera) -> None:
        for x, y, width, height, kind, angle in self.rocks:
            if not camera.sees((x, y), max(width, height)):
                continue
            sx, sy = camera.world_to_screen((x, y))
            image = scaled_sprite(self.rock_sprites[kind], (width, height))
            image = rotated_sprite(image, angle)
            screen.blit(image, image.get_rect(midbottom=(sx, sy)))

    def _draw_seaweed(self, screen: pygame.Surface, camera: Camera) -> None:
        for x, base_y, height, phase, kind in self.seaweed:
            if not camera.sees((x, base_y - height / 2), height):
                continue
            sx = round(x - camera.x * 1.035)
            sy = round(base_y - camera.y)
            source = self.plant_sprites[kind]
            image = scaled_sprite(
                source,
                (round(height * source.get_width() / source.get_height()), height),
            )
            angle = math.sin(self.time * 0.8 + phase) * 7
            image = rotated_sprite(image, angle)
            screen.blit(image, image.get_rect(midbottom=(sx, sy)))

    def _draw_coral(self, screen: pygame.Surface, camera: Camera) -> None:
        color_step = round(self.reef_health * 10)
        for x, base_y, kind, width, height, phase in self.coral:
            if not camera.sees((x, base_y - height / 2), max(width, height)):
                continue
            sx, sy = camera.world_to_screen((x, base_y))
            image = scaled_sprite(self.coral_variants[kind][color_step], (width, height))
            angle = math.sin(self.time * 0.7 + phase) * 2
            image = rotated_sprite(image, angle)
            screen.blit(image, image.get_rect(midbottom=(sx, sy)))

    def _draw_fish(self, screen: pygame.Surface, camera: Camera) -> None:
        for x, y, travel, speed, species, phase, size in self.fish:
            offset_x = math.sin(self.time * speed + phase) * travel
            offset_y = math.sin(self.time * speed * 0.8 + phase) * 13
            world_position = (x + offset_x, y + offset_y)
            if not camera.sees(world_position, 35):
                continue
            sx, sy = camera.world_to_screen(world_position)
            direction = 1 if math.cos(self.time * speed + phase) >= 0 else -1
            base = self.fish_sprites[species] if direction > 0 else self.fish_left_sprites[species]
            width = round(size * 2.5)
            height = round(width * base.get_height() / base.get_width())
            image = scaled_sprite(base, (width, height))
            image = rotated_sprite(image, math.sin(self.time * speed * 2 + phase) * 4)
            screen.blit(image, image.get_rect(center=(sx, sy)))

    def _draw_bubbles(self, screen: pygame.Surface, camera: Camera) -> None:
        for x, y, _, _ in self.bubbles:
            if not camera.sees((x, y), 12):
                continue
            sx, sy = camera.world_to_screen((x, y))
            pygame.draw.circle(screen, (155, 232, 231), (sx, sy), 3, 1)
            pygame.draw.circle(screen, (218, 255, 249), (sx - 1, sy - 1), 1)

    @staticmethod
    def habitat_color(y: float) -> tuple[int, int, int]:
        """Public helper for callers that need the region's water color."""
        return water_color_at(y)

    @staticmethod
    def habitat_zones() -> tuple[HabitatZone, ...]:
        return ZONES
