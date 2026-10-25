"""World-placed wildlife observation points and discovery tracking."""

import math
import random

import pygame

from art import load_sprite, scaled_sprite
import settings
from camera import Camera
from region_data import REGION_WILDLIFE_PROFILES, normalize_region_id


class WildlifeSystem:
    def __init__(self, region_id: str = "gulf") -> None:
        self.region_id = normalize_region_id(region_id)
        self.profiles = REGION_WILDLIFE_PROFILES[self.region_id]
        self.organisms = [
            profile for profile in self.profiles
            if profile["id"] != "plastic_bottle" and profile["position"] != (0, 0)
        ]
        self.discovered: set[str] = set()
        self.open_profile: dict[str, object] | None = None
        self.prompt_font = pygame.font.SysFont("Avenir Next", 19, bold=True)
        self.time = 0.0

    def reset(self) -> None:
        self.discovered.clear()
        self.open_profile = None
        self.time = 0.0

    def update(self, dt: float) -> None:
        self.time += dt

    def nearby(self, position: tuple[float, float]) -> dict[str, object] | None:
        closest = None
        closest_distance = settings.WILDLIFE_OBSERVE_RADIUS
        for index, organism in enumerate(self.organisms):
            x, y = self.position_of(organism, index)
            distance = math.hypot(position[0] - x, position[1] - y)
            if distance <= closest_distance:
                closest = organism
                closest_distance = distance
        return closest

    def position_of(
        self,
        profile: dict[str, object],
        index: int | None = None,
    ) -> tuple[float, float]:
        """Return the stable world position, including gentle animal patrol."""
        x, y = profile["position"]
        if profile["kind"] != "animal":
            return float(x), float(y)
        if index is None:
            index = self.organisms.index(profile)
        phase = index * 1.7
        if profile["id"] == "bottlenose_dolphin":
            return (
                float(x) + math.sin(self.time * 1.3 + phase) * 300,
                float(y) + math.sin(self.time * 2.1 + phase) * 85,
            )
        if profile["id"] == "bull_shark":
            return (
                float(x) + math.sin(self.time * 0.34 + phase) * 145,
                float(y) + math.sin(self.time * 0.53 + phase) * 34,
            )
        if profile["id"] == "sperm_whale":
            segment_duration = 7.0
            segment = int(self.time // segment_duration)
            progress = (self.time / segment_duration) - segment
            start_x, start_y = self._whale_waypoint(index, segment)
            end_x, end_y = self._whale_waypoint(index, segment + 1)
            eased_progress = progress * progress * (3 - 2 * progress)
            return (
                float(x) + start_x + (end_x - start_x) * eased_progress,
                float(y) + start_y + (end_y - start_y) * eased_progress,
            )
        segment_duration = 18.0
        segment = int(self.time // segment_duration)
        progress = (self.time / segment_duration) - segment
        start_x, start_y = self._animal_waypoint(index, segment)
        end_x, end_y = self._animal_waypoint(index, segment + 1)
        eased_progress = progress * progress * (3 - 2 * progress)
        return (
            float(x) + start_x + (end_x - start_x) * eased_progress,
            float(y) + start_y + (end_y - start_y) * eased_progress,
        )

    @staticmethod
    def _whale_waypoint(index: int, step: int) -> tuple[float, float]:
        generator = random.Random(index * 1009 + step)
        return generator.uniform(-250, 250), generator.uniform(-85, 85)

    @staticmethod
    def _animal_waypoint(index: int, step: int) -> tuple[float, float]:
        generator = random.Random(index * 1009 + step + 7919)
        return generator.uniform(-85, 85), generator.uniform(-28, 28)

    def profile_for(self, profile_id: str) -> dict[str, object]:
        return next(profile for profile in self.profiles if profile["id"] == profile_id)

    def open_info(self, profile: dict[str, object]) -> None:
        self.open_profile = profile
        self.discovered.add(str(profile["id"]))

    def observe_nearby(self, position: tuple[float, float]) -> bool:
        organism = self.nearby(position)
        if organism is None:
            return False
        self.open_info(organism)
        return True

    def close_card(self) -> None:
        self.open_profile = None

    def draw(
        self,
        screen: pygame.Surface,
        camera: Camera,
        time: float,
        hitboxes: list[tuple[pygame.Rect, dict[str, object]]] | None = None,
    ) -> None:
        for index, organism in enumerate(self.organisms):
            world_x, world_y = self.position_of(organism, index)
            hit_width, hit_height = self._illustration_hitbox_size(
                str(organism["illustration"])
            )
            if not camera.sees(
                (world_x, world_y),
                max(70, hit_width // 2, hit_height // 2),
            ):
                continue
            x, y = camera.world_to_screen((world_x, world_y))
            bob = round(math.sin(time * 1.7 + index) * 3) if organism["kind"] != "animal" else 0
            y += bob
            hitbox = pygame.Rect(
                x - hit_width // 2,
                y - hit_height // 2,
                hit_width,
                hit_height,
            )
            if hitboxes is not None:
                hitboxes.append((hitbox, organism))
            if organism["id"] == "bottlenose_dolphin":
                facing_left = math.cos(self.time * 1.3 + index * 1.7) < 0
            elif organism["id"] == "bull_shark":
                facing_left = math.cos(self.time * 0.34 + index * 1.7) < 0
            elif organism["id"] == "sperm_whale":
                segment = int(self.time // 7.0)
                facing_left = (
                    self._whale_waypoint(index, segment + 1)[0]
                    < self._whale_waypoint(index, segment)[0]
                )
            else:
                segment = int(self.time // 18.0)
                facing_left = (
                    self._animal_waypoint(index, segment + 1)[0]
                    < self._animal_waypoint(index, segment)[0]
                )
            if organism["id"] != "rocky_arch":
                self.draw_card_illustration(
                    screen,
                    organism,
                    (x, y),
                    time,
                    facing_left,
                    large_world_sprite=True,
                )

    @staticmethod
    def _illustration_hitbox_size(illustration: str) -> tuple[int, int]:
        sizes = {
            "dolphin": (148, 94),
            "jellyfish": (64, 86),
            "blue_tang": (88, 62),
            "queen_angelfish": (88, 62),
            "turtle": (78, 70),
            "loggerhead": (78, 70),
            "snapper": (94, 66),
            "whale": (360, 156),
            "shark": (108, 68),
            "coral": (80, 70),
            "reef": (82, 70),
            "seagrass": (68, 78),
            "posidonia": (78, 92),
            "arch": (150, 112),
            "amphora": (58, 72),
            "sea_bream": (96, 66),
            "grouper": (104, 72),
            "sardine": (86, 56),
            "octopus": (86, 78),
            "med_rock": (120, 82),
            "arctic_cod": (124, 65),
            "polar_cod": (124, 65),
            "arctic_char": (124, 65),
            "narwhal": (156, 80),
            "ringed_seal": (112, 70),
            "lions_mane": (72, 90),
            "arctic_kelp": (136, 150),
            "ice_shelf": (200, 110),
            "lake_sturgeon": (150, 68),
            "lake_trout": (130, 66),
            "yellow_perch": (118, 64),
            "muskellunge": (150, 68),
            "sea_lamprey": (120, 48),
            "wild_rice": (92, 140),
            "mussels": (108, 68),
            "shipwreck": (180, 120),
            "zebra_mussels": (90, 70),
            "arapaima": (152, 70),
            "piranha": (120, 65),
            "tambaqui": (140, 68),
            "boto": (170, 82),
            "river_turtle": (106, 80),
            "black_caiman": (170, 70),
            "water_lily": (110, 85),
            "flooded_forest": (180, 140),
            "forest_roots": (160, 140),
            "amazon_rock": (160, 104),
            "bottle": (58, 58),
            "can": (58, 58),
            "oil": (96, 58),
            "net": (82, 58),
        }
        return sizes.get(illustration, (92, 84))

    @staticmethod
    def _draw_dolphin(screen: pygame.Surface, x: int, y: int) -> None:
        color = (113, 193, 208)
        pygame.draw.ellipse(screen, color, (x - 31, y - 13, 61, 27))
        pygame.draw.polygon(screen, color, [(x + 25, y - 5), (x + 43, y - 15), (x + 38, y + 1)])
        pygame.draw.polygon(screen, color, [(x - 3, y - 10), (x + 7, y - 23), (x + 14, y - 8)])
        pygame.draw.circle(screen, (20, 53, 78), (x + 19, y - 4), 2)

    @staticmethod
    def _draw_turtle(screen: pygame.Surface, x: int, y: int) -> None:
        pygame.draw.ellipse(screen, (73, 156, 123), (x - 20, y - 13, 40, 27))
        pygame.draw.circle(screen, (139, 197, 133), (x + 24, y - 2), 8)
        pygame.draw.ellipse(screen, (105, 184, 141), (x - 19, y - 21, 12, 21))
        pygame.draw.ellipse(screen, (105, 184, 141), (x - 18, y + 6, 12, 20))
        pygame.draw.ellipse(screen, (105, 184, 141), (x + 3, y - 21, 12, 20))
        pygame.draw.ellipse(screen, (105, 184, 141), (x + 3, y + 7, 12, 20))

    @staticmethod
    def _draw_snapper(screen: pygame.Surface, x: int, y: int) -> None:
        body = (211, 84, 82)
        pygame.draw.ellipse(screen, body, (x - 24, y - 15, 48, 30))
        pygame.draw.polygon(screen, (245, 154, 110), [(x - 20, y), (x - 37, y - 13), (x - 37, y + 13)])
        pygame.draw.polygon(screen, (231, 119, 98), [(x - 4, y - 12), (x + 4, y - 23), (x + 11, y - 10)])
        pygame.draw.circle(screen, (35, 47, 61), (x + 15, y - 4), 2)
        pygame.draw.line(screen, (120, 42, 56), (x + 19, y + 5), (x + 25, y + 6), 2)

    @staticmethod
    def _draw_whale(screen: pygame.Surface, x: int, y: int) -> None:
        body = (100, 139, 157)
        pygame.draw.ellipse(screen, body, (x - 43, y - 18, 83, 36))
        pygame.draw.polygon(screen, body, [(x + 33, y - 4), (x + 52, y - 18), (x + 48, y + 5)])
        pygame.draw.polygon(screen, (76, 112, 132), [(x - 7, y - 14), (x + 1, y - 23), (x + 8, y - 13)])
        pygame.draw.ellipse(screen, (218, 226, 215), (x - 12, y + 6, 37, 9))
        pygame.draw.circle(screen, (25, 47, 61), (x + 27, y - 7), 2)
        pygame.draw.arc(screen, (176, 224, 232), (x + 22, y - 34, 20, 19), 4.7, 5.8, 2)

    @staticmethod
    def _draw_shark(screen: pygame.Surface, x: int, y: int) -> None:
        body = (111, 146, 160)
        pygame.draw.ellipse(screen, body, (x - 34, y - 15, 67, 30))
        pygame.draw.polygon(screen, body, [(x + 25, y - 3), (x + 47, y - 17), (x + 42, y + 5)])
        pygame.draw.polygon(screen, (82, 119, 139), [(x - 6, y - 13), (x + 1, y - 29), (x + 12, y - 12)])
        pygame.draw.polygon(screen, (91, 126, 144), [(x - 8, y + 9), (x - 1, y + 23), (x + 7, y + 9)])
        pygame.draw.ellipse(screen, (216, 225, 217), (x - 15, y + 3, 35, 9))
        pygame.draw.circle(screen, (21, 43, 58), (x + 21, y - 6), 2)

    @staticmethod
    def _draw_coral(screen: pygame.Surface, x: int, y: int) -> None:
        color = (255, 143, 136)
        pygame.draw.line(screen, color, (x, y + 23), (x, y - 18), 8)
        pygame.draw.line(screen, color, (x, y + 4), (x - 19, y - 14), 6)
        pygame.draw.line(screen, color, (x - 19, y - 14), (x - 23, y - 27), 5)
        pygame.draw.line(screen, color, (x, y - 3), (x + 19, y - 19), 6)
        pygame.draw.line(screen, color, (x + 19, y - 19), (x + 24, y - 31), 5)
        pygame.draw.circle(screen, color, (x - 23, y - 27), 4)
        pygame.draw.circle(screen, color, (x + 24, y - 31), 4)

    @staticmethod
    def _draw_reef(screen: pygame.Surface, x: int, y: int) -> None:
        pygame.draw.ellipse(screen, (105, 117, 116), (x - 36, y + 10, 72, 23))
        WildlifeSystem._draw_coral(screen, x, y)
        pygame.draw.circle(screen, (255, 189, 94), (x + 27, y - 2), 6)

    @staticmethod
    def _draw_seagrass(screen: pygame.Surface, x: int, y: int, time: float) -> None:
        for blade in range(5):
            sway = math.sin(time * 1.2 + blade) * 7
            base_x = x - 18 + blade * 9
            pygame.draw.lines(
                screen,
                (60, 177, 130),
                False,
                [(base_x, y + 22), (round(base_x + sway), y + 5), (round(base_x - sway), y - 18 - blade % 3 * 4)],
                4,
            )

    @staticmethod
    def _draw_bottle(screen: pygame.Surface, x: int, y: int) -> None:
        pygame.draw.rect(screen, (103, 207, 183), (x - 7, y - 14, 14, 30), border_radius=4)
        pygame.draw.rect(screen, (205, 240, 216), (x - 4, y - 19, 8, 6), border_radius=2)
        pygame.draw.rect(screen, (65, 149, 142), (x - 5, y - 2, 10, 3))

    @staticmethod
    def _draw_can(screen: pygame.Surface, x: int, y: int) -> None:
        pygame.draw.rect(screen, (189, 180, 142), (x - 10, y - 13, 20, 27), border_radius=5)
        pygame.draw.ellipse(screen, (226, 217, 178), (x - 10, y - 15, 20, 6))
        pygame.draw.ellipse(screen, (132, 126, 108), (x - 10, y + 9, 20, 6))
        pygame.draw.line(screen, (248, 238, 202), (x - 5, y - 6), (x + 5, y - 6), 2)

    @staticmethod
    def _draw_oil(screen: pygame.Surface, x: int, y: int, time: float) -> None:
        pygame.draw.ellipse(screen, (27, 40, 55), (x - 37, y - 12, 74, 22))
        pygame.draw.arc(screen, (188, 137, 184), (x - 30, y - 10, 54, 16), 0.1, 2.5 + math.sin(time) * 0.1, 2)
        pygame.draw.arc(screen, (96, 188, 190), (x - 16, y - 8, 42, 12), 2.4, 5.8, 2)

    @staticmethod
    def _draw_net(screen: pygame.Surface, x: int, y: int) -> None:
        net_rect = pygame.Rect(x - 25, y - 19, 50, 38)
        pygame.draw.rect(screen, (207, 174, 106), net_rect, 2)
        for offset in range(-17, 18, 9):
            pygame.draw.line(screen, (219, 193, 133), (x + offset, y - 18), (x + offset, y + 18), 1)
        for offset in range(-12, 18, 9):
            pygame.draw.line(screen, (219, 193, 133), (x - 24, y + offset), (x + 24, y + offset), 1)

    def draw_prompt(self, screen: pygame.Surface, nearby: dict[str, object] | None) -> None:
        if nearby is None or self.open_profile is not None:
            return
        label = self.prompt_font.render("Click to learn  |  Approach and press F for info", True, settings.WHITE)
        rect = label.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT - 60))
        panel = rect.inflate(28, 18)
        pygame.draw.rect(screen, (5, 39, 63), panel, border_radius=10)
        screen.blit(label, rect)

    @staticmethod
    def draw_card_illustration(
        screen: pygame.Surface,
        profile: dict[str, object],
        center: tuple[int, int],
        time: float = 0.0,
        facing_left: bool = False,
        large_world_sprite: bool = False,
    ) -> None:
        """Draw the same recognizable artwork in the world and its information card."""
        x, y = center
        illustration = str(profile["illustration"])
        sprites = {
            "dolphin": ("animals", "bottlenose_dolphin", (110, 66)),
            "jellyfish": ("animals", "moon_jellyfish", (52, 72)),
            "med_jellyfish": ("animals", "mediterranean_moon_jellyfish", (52, 72)),
            "blue_tang": ("fish", "blue_tang", (78, 54)),
            "queen_angelfish": ("fish", "queen_angelfish", (78, 54)),
            "sargassum": ("plants", "sargassum", (66, 73)),
            "turtle": ("animals", "green_sea_turtle", (76, 68)),
            "loggerhead": ("animals", "loggerhead_turtle", (76, 68)),
            "snapper": ("fish", "red_snapper", (92, 64)),
            "whale": (
                "animals",
                "sperm_whale",
                (340, 136) if large_world_sprite else (126, 50),
            ),
            "shark": ("animals", "bull_shark", (106, 64)),
            "coral": ("coral", "branching_coral", (78, 66)),
            "sea_bream": ("fish", "white_seabream", (88, 58)),
            "grouper": ("fish", "dusky_grouper", (98, 64)),
            "sardine": ("fish", "european_sardine", (82, 54)),
            "octopus": ("animals", "common_octopus", (82, 74)),
            "med_rock": ("terrain", "mediterranean_rock", (120, 78)),
            "arctic_cod": ("arctic", "fish", "arctic_cod", (140, 66), (92, 44)),
            "polar_cod": ("arctic", "fish", "polar_cod", (140, 66), (92, 44)),
            "arctic_char": ("arctic", "fish", "arctic_char", (140, 66), (92, 44)),
            "narwhal": ("arctic", "animals", "narwhal", (195, 92), (130, 62)),
            "ringed_seal": ("arctic", "animals", "ringed_seal", (132, 82), (90, 56)),
            "lions_mane": ("arctic", "animals", "lions_mane", (90, 110), (54, 66)),
            "arctic_kelp": ("arctic", "plants", "kelp", (160, 180), (74, 84)),
            "ice_shelf": ("arctic", "landmarks", "ice_shelf", (500, 190), (140, 54)),
            "lake_sturgeon": ("great_lakes", "fish", "lake_sturgeon", (175, 78), (110, 50)),
            "lake_trout": ("great_lakes", "fish", "lake_trout", (150, 76), (100, 52)),
            "yellow_perch": ("great_lakes", "fish", "yellow_perch", (138, 74), (92, 50)),
            "muskellunge": ("great_lakes", "animals", "muskellunge", (175, 78), (112, 50)),
            "sea_lamprey": ("great_lakes", "animals", "sea_lamprey", (135, 52), (94, 36)),
            "wild_rice": ("great_lakes", "plants", "wild_rice", (100, 152), (62, 94)),
            "mussels": ("great_lakes", "animals", "mussels", (118, 78), (76, 50)),
            "shipwreck": ("great_lakes", "landmarks", "shipwreck", (390, 230), (142, 84)),
            "zebra_mussels": ("great_lakes", "animals", "zebra_mussels", (104, 78), (72, 54)),
            "arapaima": ("amazon", "fish", "arapaima", (180, 82), (118, 54)),
            "piranha": ("amazon", "fish", "piranha", (140, 76), (94, 52)),
            "tambaqui": ("amazon", "fish", "tambaqui", (160, 78), (104, 52)),
            "boto": ("amazon", "animals", "boto", (190, 92), (130, 64)),
            "river_turtle": ("amazon", "animals", "river_turtle", (120, 90), (82, 62)),
            "black_caiman": ("amazon", "animals", "black_caiman", (190, 80), (130, 56)),
            "water_lily": ("amazon", "plants", "water_lily", (132, 102), (78, 60)),
            "flooded_forest": ("amazon", "landmarks", "flooded_forest", (380, 280), (142, 104)),
            "forest_roots": ("amazon", "landmarks", "forest_roots", (280, 230), (132, 110)),
        }
        regional_sprites = {
            "arctic_cod": ("arctic", "fish", "arctic_cod", (140, 66), (92, 44)),
            "polar_cod": ("arctic", "fish", "polar_cod", (140, 66), (92, 44)),
            "arctic_char": ("arctic", "fish", "arctic_char", (140, 66), (92, 44)),
            "narwhal": ("arctic", "animals", "narwhal", (195, 92), (130, 62)),
            "ringed_seal": ("arctic", "animals", "ringed_seal", (132, 82), (90, 56)),
            "lions_mane": ("arctic", "animals", "lions_mane", (90, 110), (54, 66)),
            "arctic_kelp": ("arctic", "plants", "kelp", (160, 180), (74, 84)),
            "ice_shelf": ("arctic", "landmarks", "ice_shelf", (500, 190), (140, 54)),
            "lake_sturgeon": ("great_lakes", "fish", "lake_sturgeon", (175, 78), (110, 50)),
            "lake_trout": ("great_lakes", "fish", "lake_trout", (150, 76), (100, 52)),
            "yellow_perch": ("great_lakes", "fish", "yellow_perch", (138, 74), (92, 50)),
            "muskellunge": ("great_lakes", "animals", "muskellunge", (175, 78), (112, 50)),
            "sea_lamprey": ("great_lakes", "animals", "sea_lamprey", (135, 52), (94, 36)),
            "wild_rice": ("great_lakes", "plants", "wild_rice", (100, 152), (62, 94)),
            "mussels": ("great_lakes", "animals", "mussels", (118, 78), (76, 50)),
            "shipwreck": ("great_lakes", "landmarks", "shipwreck", (390, 230), (142, 84)),
            "zebra_mussels": ("great_lakes", "animals", "zebra_mussels", (104, 78), (72, 54)),
            "arapaima": ("amazon", "fish", "arapaima", (180, 82), (118, 54)),
            "piranha": ("amazon", "fish", "piranha", (140, 76), (94, 52)),
            "tambaqui": ("amazon", "fish", "tambaqui", (160, 78), (104, 52)),
            "boto": ("amazon", "animals", "boto", (190, 92), (130, 64)),
            "river_turtle": ("amazon", "animals", "river_turtle", (120, 90), (82, 62)),
            "black_caiman": ("amazon", "animals", "black_caiman", (190, 80), (130, 56)),
            "water_lily": ("amazon", "plants", "water_lily", (132, 102), (78, 60)),
            "flooded_forest": ("amazon", "landmarks", "flooded_forest", (380, 280), (142, 104)),
            "forest_roots": ("amazon", "landmarks", "forest_roots", (280, 230), (132, 110)),
            "arctic_rock": ("arctic", "terrain", "rock", (160, 104), (100, 65)),
            "great_lakes_rock": ("great_lakes", "terrain", "rock", (160, 104), (100, 65)),
            "amazon_rock": ("amazon", "terrain", "rock", (160, 104), (100, 65)),
        }
        if illustration in regional_sprites:
            region, category, name, world_size, card_size = regional_sprites[illustration]
            size = world_size if large_world_sprite else card_size
            image = scaled_sprite(
                load_sprite(f"regions/{region}/{category}", name),
                size,
            )
            if facing_left:
                image = pygame.transform.flip(image, True, False)
            screen.blit(image, image.get_rect(center=(x, y)))
            return
        if illustration in sprites:
            category, name, size = sprites[illustration]
            image = scaled_sprite(load_sprite(category, name), size)
            if facing_left:
                image = pygame.transform.flip(image, True, False)
            screen.blit(image, image.get_rect(center=(x, y)))
        elif illustration == "reef":
            rock = scaled_sprite(load_sprite("terrain", "limestone_reef"), (78, 48))
            coral = scaled_sprite(load_sprite("coral", "branching_coral"), (54, 50))
            screen.blit(rock, rock.get_rect(center=(x, y + 16)))
            screen.blit(coral, coral.get_rect(midbottom=(x, y + 18)))
        elif illustration == "seagrass":
            image = scaled_sprite(load_sprite("plants", "seagrass"), (66, 73))
            sway = round(math.sin(time * 1.3) * 5)
            screen.blit(image, image.get_rect(midbottom=(x + sway, y + 31)))
        elif illustration == "posidonia":
            image = scaled_sprite(load_sprite("plants", "posidonia"), (74, 88))
            sway = round(math.sin(time * 1.3) * 5)
            screen.blit(image, image.get_rect(midbottom=(x + sway, y + 35)))
        elif illustration == "arch":
            image = scaled_sprite(
                load_sprite("terrain", "mediterranean_rock_arch"),
                (420, 290) if large_world_sprite else (142, 100),
            )
            screen.blit(image, image.get_rect(center=(x, y)))
        elif illustration == "amphora":
            image = scaled_sprite(load_sprite("landmarks", "amphora"), (54, 66))
            screen.blit(image, image.get_rect(center=(x, y)))
        elif illustration in ("bottle", "can", "net", "oil"):
            GamePollutantIllustration.draw(screen, illustration, center)
        elif illustration.startswith("mediterranean_"):
            name = illustration.removeprefix("mediterranean_")
            image = scaled_sprite(load_sprite("pollution", f"mediterranean_{name}"), (42, 42))
            screen.blit(image, image.get_rect(center=(x, y)))


class GamePollutantIllustration:
    """Large, centered pollutant vectors used on educational information cards."""

    @staticmethod
    def draw(screen: pygame.Surface, illustration: str, center: tuple[int, int]) -> None:
        x, y = center
        if illustration == "bottle":
            pygame.draw.rect(screen, (103, 207, 183), (x - 12, y - 23, 24, 48), border_radius=7)
            pygame.draw.rect(screen, (205, 240, 216), (x - 7, y - 32, 14, 11), border_radius=3)
            pygame.draw.rect(screen, (65, 149, 142), (x - 9, y - 3, 18, 4))
        elif illustration == "can":
            pygame.draw.rect(screen, (189, 180, 142), (x - 17, y - 22, 34, 43), border_radius=8)
            pygame.draw.ellipse(screen, (226, 217, 178), (x - 17, y - 26, 34, 9))
            pygame.draw.ellipse(screen, (132, 126, 108), (x - 17, y + 16, 34, 9))
            pygame.draw.line(screen, (248, 238, 202), (x - 8, y - 8), (x + 8, y - 8), 3)
        elif illustration == "net":
            rect = pygame.Rect(x - 38, y - 25, 76, 50)
            pygame.draw.rect(screen, (207, 177, 113), rect, 3)
            for offset in range(-28, 33, 12):
                pygame.draw.line(screen, (222, 202, 148), (x + offset, y - 23), (x + offset, y + 23), 2)
            for offset in (-13, 0, 13):
                pygame.draw.line(screen, (222, 202, 148), (x - 36, y + offset), (x + 36, y + offset), 2)
        elif illustration == "oil":
            pygame.draw.ellipse(screen, (27, 40, 55), (x - 45, y - 19, 90, 38))
            pygame.draw.arc(screen, (188, 137, 184), (x - 36, y - 16, 68, 30), 0.1, 2.5, 3)
            pygame.draw.arc(screen, (96, 188, 190), (x - 18, y - 12, 51, 23), 2.4, 5.8, 3)
