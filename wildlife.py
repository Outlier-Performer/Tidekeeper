"""World-placed wildlife observation points and discovery tracking."""

import math

import pygame

from art import load_sprite, scaled_sprite
import settings
from ecology_data import WILDLIFE_PROFILES
from camera import Camera


class WildlifeSystem:
    def __init__(self) -> None:
        self.organisms = [
            profile for profile in WILDLIFE_PROFILES
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
        return (
            float(x) + math.sin(self.time * 0.42 + phase) * 46,
            float(y) + math.sin(self.time * 0.68 + phase) * 13,
        )

    def profile_for(self, profile_id: str) -> dict[str, object]:
        return next(profile for profile in WILDLIFE_PROFILES if profile["id"] == profile_id)

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
            if not camera.sees((world_x, world_y), 70):
                continue
            x, y = camera.world_to_screen((world_x, world_y))
            bob = round(math.sin(time * 1.7 + index) * 3) if organism["kind"] != "animal" else 0
            y += bob
            hit_width, hit_height = self._illustration_hitbox_size(
                str(organism["illustration"])
            )
            hitbox = pygame.Rect(
                x - hit_width // 2,
                y - hit_height // 2,
                hit_width,
                hit_height,
            )
            if hitboxes is not None:
                hitboxes.append((hitbox, organism))
            dolphin_facing_left = (
                organism["id"] in ("bottlenose_dolphin", "bull_shark")
                and math.cos(
                    self.time * (1.3 if organism["id"] == "bottlenose_dolphin" else 0.34)
                    + index * 1.7
                ) < 0
            )
            self.draw_card_illustration(
                screen,
                organism,
                (x, y),
                time,
                dolphin_facing_left,
            )

    @staticmethod
    def _illustration_hitbox_size(illustration: str) -> tuple[int, int]:
        sizes = {
            "dolphin": (148, 94),
            "jellyfish": (64, 86),
            "blue_tang": (88, 62),
            "queen_angelfish": (88, 62),
            "turtle": (78, 70),
            "snapper": (94, 66),
            "whale": (114, 70),
            "shark": (108, 68),
            "coral": (80, 70),
            "reef": (82, 70),
            "seagrass": (68, 78),
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
    ) -> None:
        """Draw the same recognizable artwork in the world and its information card."""
        x, y = center
        illustration = str(profile["illustration"])
        sprites = {
            "dolphin": ("animals", "bottlenose_dolphin", (110, 66)),
            "jellyfish": ("animals", "moon_jellyfish", (52, 72)),
            "blue_tang": ("fish", "blue_tang", (78, 54)),
            "queen_angelfish": ("fish", "queen_angelfish", (78, 54)),
            "sargassum": ("plants", "sargassum", (66, 73)),
            "turtle": ("animals", "green_sea_turtle", (76, 68)),
            "snapper": ("fish", "red_snapper", (92, 64)),
            "whale": ("animals", "sperm_whale", (112, 66)),
            "shark": ("animals", "bull_shark", (106, 64)),
            "coral": ("coral", "branching_coral", (78, 66)),
        }
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
        elif illustration in ("bottle", "can", "net", "oil"):
            GamePollutantIllustration.draw(screen, illustration, center)


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
