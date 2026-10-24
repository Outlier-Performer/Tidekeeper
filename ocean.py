"""Procedurally generated, scrolling underwater environment."""

import math
import random

import pygame

from art import load_sprite, rotated_sprite, scaled_sprite
from camera import Camera
from ecology_data import ENVIRONMENT_PROFILES
from mediterranean_data import ENVIRONMENT_PROFILES as MEDITERRANEAN_ENVIRONMENT_PROFILES
from region_data import (
    REGION_ENVIRONMENT_PROFILES,
    REGION_TINTS,
    REGION_WILDLIFE_PROFILES,
    normalize_region_id,
)
import settings
from world import HabitatZone, water_color_at, zones_for


class Ocean:
    def __init__(self, region_id: str = "gulf") -> None:
        self.region_id = normalize_region_id(region_id)
        self.is_mediterranean = self.region_id == "mediterranean"
        self.is_custom_region = self.region_id in ("arctic", "great_lakes", "amazon")
        self.time = 0.0
        self.reef_health = 0.0
        self.random = random.Random(18)
        if self.is_custom_region:
            folder = f"regions/{self.region_id}"
            self.backdrop = load_sprite(f"{folder}/backgrounds", "backdrop").copy()
            self.floor_tile = load_sprite(f"{folder}/terrain", "floor")
            self.plant_sprites = {
                name: load_sprite(f"{folder}/plants", asset)
                for name, asset in {
                    "arctic_kelp": "kelp",
                    "wild_rice": "wild_rice",
                    "water_lily": "water_lily",
                }.items()
                if (name == "arctic_kelp" and self.region_id == "arctic")
                or (name == "wild_rice" and self.region_id == "great_lakes")
                or (name == "water_lily" and self.region_id == "amazon")
            }
            self.coral_sprites = {}
            self.rock_sprites = {
                "regional": load_sprite(f"{folder}/terrain", "rock")
            }
            fish_names = {
                "arctic": ("arctic_cod", "polar_cod", "arctic_char"),
                "great_lakes": ("lake_sturgeon", "lake_trout", "yellow_perch"),
                "amazon": ("arapaima", "piranha", "tambaqui"),
            }[self.region_id]
            self.fish_sprites = {
                name: load_sprite(f"{folder}/fish", name)
                for name in fish_names
            }
            self.environment_profiles = dict(
                REGION_ENVIRONMENT_PROFILES[self.region_id]
            )
            self.environment_profiles.update(
                {
                    profile["id"]: profile
                    for profile in REGION_WILDLIFE_PROFILES[self.region_id]
                }
            )
            if self.region_id == "amazon":
                self.environment_profiles["piranha"] = self.environment_profiles[
                    "red_bellied_piranha"
                ]
            self.landmark = None
        else:
            backdrop_name = "mediterranean_backdrop" if self.is_mediterranean else "gulf_backdrop"
            floor_name = "mediterranean_sandy_floor" if self.is_mediterranean else "sandy_floor_tile"
            self.backdrop = load_sprite("backgrounds", backdrop_name).copy()
            self.floor_tile = load_sprite("terrain", floor_name)
            self.plant_sprites = (
                {"posidonia": load_sprite("plants", "posidonia")}
                if self.is_mediterranean
                else {
                    "seagrass": load_sprite("plants", "seagrass"),
                    "sargassum": load_sprite("plants", "sargassum"),
                }
            )
            self.coral_sprites = (
                {}
                if self.is_mediterranean
                else {
                    "branch": load_sprite("coral", "branching_coral"),
                    "brain": load_sprite("coral", "brain_coral"),
                    "fan": load_sprite("coral", "sea_fan"),
                }
            )
            self.rock_sprites = (
                {"mediterranean": load_sprite("terrain", "mediterranean_rock")}
                if self.is_mediterranean
                else {
                    "limestone": load_sprite("terrain", "limestone_reef"),
                    "sandstone": load_sprite("terrain", "sandstone_reef"),
                }
            )
            self.fish_sprites = (
                {
                    "sardine": load_sprite("fish", "european_sardine"),
                    "sea_bream": load_sprite("fish", "white_seabream"),
                    "grouper": load_sprite("fish", "dusky_grouper"),
                }
                if self.is_mediterranean
                else {
                    "red_snapper": load_sprite("fish", "red_snapper"),
                    "blue_tang": load_sprite("fish", "blue_tang"),
                    "queen_angelfish": load_sprite("fish", "queen_angelfish"),
                }
            )
            self.environment_profiles = (
                MEDITERRANEAN_ENVIRONMENT_PROFILES
                if self.is_mediterranean
                else ENVIRONMENT_PROFILES
            )
            self.landmark = (
                load_sprite("terrain", "mediterranean_rock_arch")
                if self.is_mediterranean
                else None
            )
        self.coral_variants = self._make_coral_variants()
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
        self.region_tint = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)
        tint = REGION_TINTS[self.region_id]
        self.region_tint.fill(tint or (0, 0, 0, 0))

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
        if self.is_custom_region:
            placements = []
            plant_name = {
                "arctic": "arctic_kelp",
                "great_lakes": "wild_rice",
                "amazon": "water_lily",
            }[self.region_id]
            meadows = {
                "arctic": ((400, 920), (1210, 1040), (2190, 1150), (3310, 980)),
                "great_lakes": ((360, 320), (850, 430), (1960, 520), (3090, 380)),
                "amazon": ((410, 230), (1160, 390), (2070, 320), (3310, 470)),
            }[self.region_id]
            for center_x, base_y in meadows:
                for _ in range(8):
                    placements.append(
                        (
                            center_x + self.random.randint(-120, 120),
                            base_y + self.random.randint(-22, 16),
                            self.random.randint(88, 154),
                            self.random.random() * math.tau,
                            plant_name,
                        )
                    )
            return placements
        if self.is_mediterranean:
            placements = []
            meadows = (
                (370, 820),
                (920, 940),
                (1470, 1060),
                (1910, 1160),
                (2680, 930),
                (3180, 1120),
                (2000, 1240),
                (3550, 1040),
            )
            for center_x, base_y in meadows:
                for _ in range(9):
                    placements.append(
                        (
                            center_x + self.random.randint(-140, 140),
                            base_y + self.random.randint(-35, 22),
                            self.random.randint(74, 132),
                            self.random.random() * math.tau,
                            "posidonia",
                        )
                    )
            return placements

        placements = []
        meadows = (
            (230, 850, "seagrass"),
            (680, 875, "seagrass"),
            (1190, 420, "sargassum"),
            (1580, 1975, "seagrass"),
            (1880, 1975, "sargassum"),
            (2480, 1980, "seagrass"),
            (2920, 620, "sargassum"),
            (3440, 1900, "seagrass"),
            (3800, 520, "sargassum"),
        )
        for center_x, base_y, kind in meadows:
            for _ in range(6):
                placements.append(
                    (
                        center_x + self.random.randint(-110, 110),
                        base_y + self.random.randint(-35, 25),
                        self.random.randint(58, 108),
                        self.random.random() * math.tau,
                        kind,
                    )
                )
        return placements

    def _make_coral(self) -> list[tuple[float, float, str, int, int, float]]:
        if self.is_mediterranean or self.is_custom_region:
            return []
        placements = []
        reef_groups = (
            (820, 1690, 4),
            (1450, 1910, 4),
            (2150, 2020, 5),
            (2900, 2020, 5),
            (3550, 1910, 4),
        )
        kinds = ("branch", "brain", "fan")
        for center_x, base_y, count in reef_groups:
            spacing = 120
            start_x = center_x - (count - 1) * spacing / 2
            for index in range(count):
                kind = kinds[(index + self.random.randrange(len(kinds))) % len(kinds)]
                scale = self.random.uniform(0.42, 0.58)
                source = self.coral_sprites[kind]
                placements.append(
                    (
                        start_x + index * spacing + self.random.randint(-9, 9),
                        base_y + self.random.randint(-8, 8),
                        kind,
                        round(source.get_width() * scale),
                        round(source.get_height() * scale),
                        self.random.uniform(-0.08, 0.08),
                    )
                )
        return placements

    def _make_rocks(self) -> list[tuple[float, float, int, int, str, float]]:
        placements = []
        if self.is_custom_region:
            rock_sites = {
                "arctic": ((120, 2030), (770, 1960), (1330, 2240), (2180, 1980), (3240, 2210), (430, 2810), (1810, 2790), (3540, 2790)),
                "great_lakes": ((110, 890), (780, 965), (1420, 1760), (2200, 2030), (3150, 1930), (460, 2780), (1890, 2790), (3500, 2750)),
                "amazon": ((160, 880), (760, 1000), (1510, 1760), (2290, 2010), (3240, 1850), (480, 2780), (1870, 2790), (3520, 2780)),
            }[self.region_id]
            for index, (center_x, base_y) in enumerate(rock_sites):
                placements.append(
                    (
                        center_x + self.random.randint(-70, 70),
                        base_y + self.random.randint(-16, 18),
                        round(self.random.uniform(140, 190)),
                        round(self.random.uniform(76, 110)),
                        "regional",
                        self.random.random() * 7 - 3.5,
                    )
                )
            return placements
        if self.is_mediterranean:
            rock_sites = (
                (100, 890),
                (700, 980),
                (1280, 1770),
                (1880, 2030),
                (2250, 2630),
                (2810, 2700),
                (3540, 1970),
                (450, 2820),
                (1550, 2800),
                (3680, 2780),
            )
            for index, (center_x, base_y) in enumerate(rock_sites):
                for _ in range(3 if index in (3, 4) else 2):
                    scale = self.random.uniform(0.55, 0.95)
                    placements.append(
                        (
                            center_x + self.random.randint(-75, 75),
                            base_y + self.random.randint(-16, 18),
                            round(180 * scale),
                            round(116 * scale),
                            "mediterranean",
                            self.random.random() * 8 - 4,
                        )
                    )
            return placements

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
        if self.is_custom_region:
            schools = {
                "arctic": (
                    (390, 460, "arctic_cod", 12),
                    (1120, 850, "polar_cod", 8),
                    (1760, 1450, "arctic_char", 6),
                    (2730, 980, "arctic_cod", 14),
                    (3430, 1710, "polar_cod", 10),
                ),
                "great_lakes": (
                    (350, 450, "yellow_perch", 11),
                    (1030, 1430, "lake_trout", 7),
                    (1720, 2180, "lake_sturgeon", 5),
                    (2560, 760, "yellow_perch", 12),
                    (3370, 1670, "lake_trout", 9),
                ),
                "amazon": (
                    (360, 600, "piranha", 10),
                    (1030, 1260, "tambaqui", 7),
                    (1720, 580, "arapaima", 5),
                    (2550, 950, "piranha", 12),
                    (3370, 1710, "tambaqui", 9),
                ),
            }[self.region_id]
        elif self.is_mediterranean:
            schools = (
                (330, 460, "sardine", 13),
                (930, 690, "sea_bream", 7),
                (1540, 1420, "sardine", 15),
                (2320, 1690, "grouper", 5),
                (2950, 1290, "sea_bream", 7),
                (3510, 1710, "sardine", 12),
                (1760, 2310, "grouper", 4),
            )
        else:
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
        self._draw_landmark(screen, camera)
        self._draw_seaweed(screen, camera)
        self._draw_coral(screen, camera)
        self._draw_fish(screen, camera)
        self._draw_bubbles(screen, camera)
        if self.region_id != "gulf":
            screen.blit(self.region_tint, (0, 0))

    def info_hitboxes(self, camera: Camera) -> list[tuple[pygame.Rect, dict[str, object]]]:
        hitboxes: list[tuple[pygame.Rect, dict[str, object]]] = []
        for x, y, kind, width, height, phase in self.coral:
            if camera.sees((x, y - height / 2), max(width, height)):
                sx, sy = camera.world_to_screen((x, y))
                image = scaled_sprite(self.coral_variants[kind][10], (width, height))
                image = rotated_sprite(image, math.sin(self.time * 0.7 + phase) * 2)
                hitboxes.append(
                    (image.get_rect(midbottom=(sx, sy)), self.environment_profiles["coral"])
                )

        for x, y, width, height, *_ in self.rocks:
            if camera.sees((x, y), max(width, height)):
                sx, sy = camera.world_to_screen((x, y))
                hitboxes.append(
                    (
                        pygame.Rect(sx - width // 2, sy - height, width, height),
                        self.environment_profiles.get(
                            "rock",
                            self.environment_profiles.get(
                                "reef",
                                next(iter(self.environment_profiles.values())),
                            ),
                        ),
                    )
                )

        for x, base_y, height, phase, kind in self.seaweed:
            if not camera.sees((x, base_y - height / 2), height):
                continue
            source = self.plant_sprites[kind]
            size = (
                round(height * source.get_width() / source.get_height()),
                height,
            )
            image = scaled_sprite(source, size)
            image = rotated_sprite(image, math.sin(self.time * 0.8 + phase) * 7)
            sx = round(x - camera.x * 1.035)
            sy = round(base_y - camera.y)
            profile = self.environment_profiles[kind]
            hitboxes.append((image.get_rect(midbottom=(sx, sy)), profile))

        for x, y, travel, speed, species, phase, size in self.fish:
            offset_x = math.sin(self.time * speed + phase) * travel
            offset_y = math.sin(self.time * speed * 0.8 + phase) * 13
            world_position = (x + offset_x, y + offset_y)
            if not camera.sees(world_position, 35):
                continue
            sx, sy = camera.world_to_screen(world_position)
            base = self.fish_sprites[species]
            width = round(size * 2.5)
            height = round(width * base.get_height() / base.get_width())
            image = scaled_sprite(base, (width, height))
            image = rotated_sprite(image, math.sin(self.time * speed * 2 + phase) * 4)
            hitboxes.append(
                (
                    image.get_rect(center=(sx, sy)),
                    self.environment_profiles[species],
                )
            )
        return hitboxes

    def _draw_landmark(self, screen: pygame.Surface, camera: Camera) -> None:
        if self.landmark is None:
            return
        position = (2460, 2730)
        if not camera.sees(position, 440):
            return
        x, y = camera.world_to_screen(position)
        image = scaled_sprite(self.landmark, (420, 290))
        screen.blit(image, image.get_rect(midbottom=(x, y)))

    def _draw_water(self, screen: pygame.Surface, camera: Camera) -> None:
        band_height = 12
        for top in range(0, settings.HEIGHT, band_height):
            world_y = camera.y + top + band_height / 2
            color = list(water_color_at(world_y, self.region_id))
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
        ray_color = {
            "gulf": (149, 240, 225),
            "mediterranean": (194, 240, 246),
            "arctic": (225, 246, 255),
            "great_lakes": (170, 230, 210),
            "amazon": (248, 197, 166),
        }[self.region_id]
        for index in range(5):
            x = int(65 + index * 230 + math.sin(self.time * 0.2 + index) * 34)
            width = 25 + int(self.reef_health * 9)
            pygame.draw.polygon(
                self.light_layer,
                (*ray_color, alpha),
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
        surface_color = {
            "gulf": (98, 218, 207),
            "mediterranean": (156, 201, 207),
            "arctic": (227, 241, 246),
            "great_lakes": (117, 198, 192),
            "amazon": (206, 151, 137),
        }[self.region_id]
        glint_color = {
            "gulf": (181, 250, 232),
            "mediterranean": (228, 189, 191),
            "arctic": (255, 255, 255),
            "great_lakes": (205, 242, 224),
            "amazon": (255, 203, 185),
        }[self.region_id]
        pygame.draw.rect(screen, surface_color, (0, surface_y, settings.WIDTH, 6))
        for index in range(18):
            x = index * 61 + int(self.time * 12) % 61
            wave_y = surface_y + round(math.sin(index + self.time * 1.5) * 4)
            pygame.draw.arc(screen, glint_color, (x, wave_y - 4, 70, 13), 0.2, 2.8, 2)

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
            outline, highlight = {
                "gulf": ((155, 232, 231), (218, 255, 249)),
                "mediterranean": ((217, 177, 190), (255, 230, 224)),
                "arctic": ((221, 246, 255), (255, 255, 255)),
                "great_lakes": ((175, 229, 216), (234, 255, 243)),
                "amazon": ((245, 164, 162), (255, 222, 197)),
            }[self.region_id]
            pygame.draw.circle(screen, outline, (sx, sy), 3, 1)
            pygame.draw.circle(screen, highlight, (sx - 1, sy - 1), 1)

    @staticmethod
    def habitat_color(y: float, region_id: str = "gulf") -> tuple[int, int, int]:
        """Public helper for callers that need the region's water color."""
        return water_color_at(y, region_id)

    @staticmethod
    def habitat_zones(region_id: str = "gulf") -> tuple[HabitatZone, ...]:
        return zones_for(region_id)
