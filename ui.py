"""Menu, fixed HUD, and source-linked point-of-interest cards."""

import pygame

from art import load_sprite, scaled_sprite
import settings
from region_data import (
    REGION_HAZARD_NAMES,
    REGION_IDS,
    REGION_LABELS,
    normalize_region_id,
)
from wildlife import WildlifeSystem


class GameUI:
    def __init__(self) -> None:
        self.title_font = pygame.font.SysFont("Avenir Next", 62, bold=True)
        self.heading_font = pygame.font.SysFont("Avenir Next", 37, bold=True)
        self.body_font = pygame.font.SysFont("Avenir Next", 22)
        self.small_font = pygame.font.SysFont("Avenir Next", 18)
        self.menu_font = pygame.font.SysFont("Avenir Next", 29, bold=True)
        button_width = 380
        button_height = 66
        left_x = settings.WIDTH // 2 - 400
        right_x = settings.WIDTH // 2 + 20
        row_y = (292, 376, 460)
        positions = {
            "gulf": (left_x, row_y[0]),
            "mediterranean": (right_x, row_y[0]),
            "arctic": (left_x, row_y[1]),
            "great_lakes": (right_x, row_y[1]),
            "amazon": (settings.WIDTH // 2 - button_width // 2, row_y[2]),
        }
        self.region_button_rects = {
            region_id: pygame.Rect(*positions[region_id], button_width, button_height)
            for region_id in REGION_IDS
        }
        self.explore_button_rect = pygame.Rect(settings.WIDTH // 2 - 215, 300, 430, 76)
        self.play_button_rect = pygame.Rect(settings.WIDTH // 2 - 215, 396, 430, 76)
        self.back_button_rect = pygame.Rect(settings.WIDTH // 2 - 110, 506, 220, 54)
        self.start_button_rect = self.explore_button_rect
        self.difficulty_button_rects = {
            "easy": pygame.Rect(145, 350, 220, 88),
            "medium": pygame.Rect(390, 350, 220, 88),
            "hard": pygame.Rect(635, 350, 220, 88),
        }
        self.source_link_rect: pygame.Rect | None = None

    @staticmethod
    def _text(screen, font, text, color, center) -> None:
        image = font.render(text, True, color)
        screen.blit(image, image.get_rect(center=center))

    def _draw_menu_panel(self, screen: pygame.Surface) -> pygame.Rect:
        panel = pygame.Rect(70, 115, 860, 470)
        pygame.draw.rect(screen, (3, 29, 50, 218), panel, border_radius=26)
        pygame.draw.rect(screen, (153, 194, 198, 130), panel, 1, border_radius=26)
        return panel

    def _draw_menu_button(
        self,
        screen: pygame.Surface,
        rect: pygame.Rect,
        label: str,
        selected: bool = False,
        hovered: bool = False,
        region_id: str = "gulf",
    ) -> None:
        palette = {
            "gulf": ((202, 145, 98), (107, 133, 124), (255, 229, 188)),
            "mediterranean": ((174, 103, 111), (119, 75, 88), (255, 218, 214)),
            "arctic": ((173, 211, 229), (96, 132, 151), (232, 248, 255)),
            "great_lakes": ((98, 194, 176), (63, 128, 129), (213, 248, 234)),
            "amazon": ((231, 155, 141), (148, 91, 91), (255, 224, 207)),
        }
        selected_color, color, outline = palette.get(region_id, palette["gulf"])
        if selected:
            color = selected_color
        if hovered:
            color = tuple(min(255, channel + 18) for channel in color)
        pygame.draw.rect(screen, color, rect, border_radius=15)
        if selected:
            pygame.draw.rect(screen, outline, rect, 2, border_radius=15)
        label_image = self.menu_font.render(label, True, settings.WHITE)
        screen.blit(label_image, label_image.get_rect(center=rect.center))

    def draw_region_select(
        self,
        screen: pygame.Surface,
        mouse_position: tuple[int, int],
    ) -> None:
        self._draw_menu_panel(screen)
        self._text(
            screen,
            self.title_font,
            "TIDEKEEPER",
            settings.WHITE,
            (settings.WIDTH // 2, 225),
        )
        for region_id, rect in self.region_button_rects.items():
            self._draw_menu_button(
                screen,
                rect,
                REGION_LABELS[region_id],
                hovered=rect.collidepoint(mouse_position),
                region_id=region_id,
            )

    def draw_activity_select(
        self,
        screen: pygame.Surface,
        mouse_position: tuple[int, int],
        region_id: str,
    ) -> None:
        region_id = normalize_region_id(region_id)
        self._draw_menu_panel(screen)
        title = REGION_LABELS[region_id]
        self._text(
            screen,
            self.heading_font,
            title,
            settings.WHITE,
            (settings.WIDTH // 2, 226),
        )
        for rect, label in (
            (self.explore_button_rect, "EXPLORE"),
            (self.play_button_rect, "PLAY"),
            (self.back_button_rect, "BACK"),
        ):
            self._draw_menu_button(
                screen,
                rect,
                label,
                hovered=rect.collidepoint(mouse_position),
                region_id=region_id,
            )

    def draw_menu(
        self,
        screen: pygame.Surface,
        mouse_position: tuple[int, int],
        current_region: str = "gulf",
    ) -> None:
        self.draw_region_select(screen, mouse_position)

    def draw_difficulty_select(
        self,
        screen: pygame.Surface,
        mouse_position: tuple[int, int],
        region_id: str = "gulf",
    ) -> None:
        panel = pygame.Surface((860, 360), pygame.SRCALPHA)
        pygame.draw.rect(panel, (3, 29, 50, 218), panel.get_rect(), border_radius=26)
        pygame.draw.rect(panel, (103, 211, 204, 100), panel.get_rect(), 1, border_radius=26)
        screen.blit(panel, (70, 170))
        self._text(
            screen,
            self.heading_font,
            "CHOOSE YOUR DIFFICULTY",
            settings.WHITE,
            (settings.WIDTH // 2, 238),
        )
        hazard_name = REGION_HAZARD_NAMES[normalize_region_id(region_id)]
        descriptions = {
            "easy": ("EASY", f"12 pieces  |  7 {hazard_name}"),
            "medium": ("MEDIUM", f"18 pieces  |  10 {hazard_name}"),
            "hard": ("HARD", f"24 pieces  |  14 {hazard_name}"),
        }
        colors = {
            "easy": (94, 194, 158),
            "medium": (235, 173, 91),
            "hard": (211, 105, 104),
        }
        for difficulty, rect in self.difficulty_button_rects.items():
            color = colors[difficulty]
            if rect.collidepoint(mouse_position):
                color = tuple(min(255, channel + 24) for channel in color)
            pygame.draw.rect(screen, color, rect, border_radius=16)
            title, description = descriptions[difficulty]
            self._text(screen, self.body_font, title, settings.INK, (rect.centerx, rect.y + 30))
            self._text(screen, self.small_font, description, settings.INK, (rect.centerx, rect.y + 62))
        self._text(
            screen,
            self.small_font,
            "Predators move faster and pursue you from farther away on harder settings.",
            settings.PALE_AQUA,
            (settings.WIDTH // 2, 477),
        )
        self._text(
            screen,
            self.small_font,
            "Click a setting or press 1, 2, or 3  |  ESC to close",
            settings.WHITE,
            (settings.WIDTH // 2, 514),
        )

    def draw_hud(
        self,
        screen: pygame.Surface,
        health: int,
        score: int,
        reef_health: float,
        time_left: float,
        mode: str,
        habitat: str,
        depth: int,
        discoveries: int,
        target_score: int | None = None,
        boost_energy: float = 1.0,
        region_title: str = "GULF REEF",
    ) -> None:
        pygame.draw.rect(screen, (4, 38, 65), (0, 0, settings.WIDTH, settings.HUD_HEIGHT))
        pygame.draw.line(screen, (84, 198, 193), (0, settings.HUD_HEIGHT - 2), (settings.WIDTH, settings.HUD_HEIGHT - 2), 2)
        self._text(screen, self.small_font, region_title, settings.WHITE, (132, 18))
        timer_label = f"TIME {max(0, int(time_left + 0.999)):03d}s" if mode == "play" else "TIME PAUSED"
        self._text(screen, self.small_font, timer_label, settings.WHITE, (900, 18))
        if mode == "explore":
            self._text(screen, self.small_font, "CLICK TO LEARN  |  Inspect: press F", settings.WHITE, (474, 18))
            self._text(screen, self.small_font, "ESC: MENU", settings.PALE_AQUA, (84, 58))
            self._text(
                screen,
                self.small_font,
                f"{habitat}  |  game ~{depth}m",
                settings.PALE_AQUA,
                (370, 58),
            )
            self._text(
                screen,
                self.small_font,
                f"NOTES {discoveries}",
                settings.WHITE,
                (600, 58),
            )
            self._draw_boost_bar(screen, boost_energy, label_x=705, bar_x=746, y=51)
            return

        self._text(screen, self.small_font, "HEALTH", settings.PALE_AQUA, (42, 58))
        for index in range(settings.PLAYER_STARTING_HEALTH):
            color = settings.HEART_RED if index < health else (88, 111, 122)
            self._draw_heart(screen, 96 + index * 26, 57, color)
        target = settings.TARGET_SCORE if target_score is None else target_score
        self._text(screen, self.small_font, f"CLEANED {score}/{target}", settings.WHITE, (253, 58))
        habitat_label = "MEADOW" if region_title == "MEDITERRANEAN SEA" else "REEF"
        self._text(screen, self.small_font, habitat_label, settings.PALE_AQUA, (375, 58))
        bar = pygame.Rect(430, 51, 110, 14)
        pygame.draw.rect(screen, (24, 74, 89), bar, border_radius=8)
        fill = bar.copy()
        fill.width = round(bar.width * max(0.0, min(1.0, reef_health)))
        if fill.width:
            pygame.draw.rect(screen, (86, 222, 177), fill, border_radius=8)
        pygame.draw.rect(screen, (118, 211, 202), bar, 2, border_radius=8)
        self._draw_boost_bar(screen, boost_energy, label_x=604, bar_x=644, y=51)

    def _draw_boost_bar(
        self,
        screen: pygame.Surface,
        energy: float,
        label_x: int = 604,
        bar_x: int = 645,
        y: int = 51,
    ) -> None:
        self._text(screen, self.small_font, "BOOST", settings.PALE_AQUA, (label_x, y + 7))
        bar = pygame.Rect(bar_x, y, 122, 14)
        pygame.draw.rect(screen, (24, 74, 89), bar, border_radius=8)
        fill = bar.copy()
        fill.width = round(bar.width * max(0.0, min(1.0, energy)))
        if fill.width:
            pygame.draw.rect(screen, (90, 216, 233), fill, border_radius=8)
        pygame.draw.rect(screen, (118, 211, 202), bar, 2, border_radius=8)

    @staticmethod
    def _draw_heart(screen: pygame.Surface, x: int, y: int, color: tuple[int, int, int]) -> None:
        pygame.draw.circle(screen, color, (x - 5, y - 4), 7)
        pygame.draw.circle(screen, color, (x + 5, y - 4), 7)
        pygame.draw.polygon(screen, color, [(x - 12, y - 1), (x + 12, y - 1), (x, y + 13)])

    def draw_zone_toast(self, screen: pygame.Surface, habitat: str) -> None:
        panel = pygame.Rect(settings.WIDTH // 2 - 190, 104, 380, 48)
        pygame.draw.rect(screen, (5, 39, 63), panel, border_radius=12)
        pygame.draw.rect(screen, (97, 211, 200), panel, 1, border_radius=12)
        self._text(screen, self.body_font, habitat, settings.WHITE, panel.center)

    def draw_discovery_card(self, screen: pygame.Surface, profile: dict[str, object]) -> pygame.Rect:
        overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)
        overlay.fill((4, 25, 49, 176))
        screen.blit(overlay, (0, 0))
        panel = pygame.Rect(settings.WIDTH // 2 - 350, settings.HEIGHT // 2 - 240, 700, 480)
        pygame.draw.rect(screen, (8, 62, 86), panel, border_radius=18)
        pygame.draw.rect(screen, (115, 229, 205), panel, 2, border_radius=18)
        is_pollutant = profile.get("kind") == "pollutant"
        if is_pollutant:
            illustration = str(profile.get("illustration", ""))
            if illustration.startswith("mediterranean_"):
                asset_name = illustration.removeprefix("mediterranean_")
                sprite = scaled_sprite(
                    load_sprite("pollution", f"mediterranean_{asset_name}"),
                    (90, 90),
                )
                screen.blit(sprite, sprite.get_rect(center=(panel.x + 59, panel.y + 56)))
            elif illustration.startswith(("arctic_", "great_lakes_", "amazon_")):
                region = next(
                    region
                    for region in ("great_lakes", "arctic", "amazon")
                    if illustration.startswith(f"{region}_")
                )
                asset_name = illustration.removeprefix(f"{region}_")
                pollutant_name = {
                    ("great_lakes", "line"): "line",
                    ("great_lakes", "can"): "can",
                    ("amazon", "lost_net"): "net",
                    ("amazon", "mining_drum"): "drum",
                    ("arctic", "ghost_net"): "net",
                    ("arctic", "fuel_canister"): "canister",
                }.get((region, asset_name), asset_name)
                sprite = scaled_sprite(
                    load_sprite(
                        f"regions/{region}/pollution",
                        pollutant_name,
                    ),
                    (90, 90),
                )
                screen.blit(sprite, sprite.get_rect(center=(panel.x + 59, panel.y + 56)))
            else:
                self._draw_pollutant_art(
                    screen,
                    illustration,
                    (panel.x + 59, panel.y + 56),
                )
        else:
            WildlifeSystem.draw_card_illustration(
                screen,
                profile,
                (panel.x + 59, panel.y + 56),
            )

        title_rect = self._fit_text(
            screen,
            self.heading_font,
            str(profile["name"]),
            settings.WHITE,
            (settings.WIDTH // 2 + 35, panel.y + 38),
            panel.width - 112,
        )
        subtitle_image = self._fit_surface(
            self.small_font,
            f'{str(profile["kind"]).upper()}  |  {profile["habitat"]}',
            settings.PALE_AQUA,
            panel.width - 60,
        )
        subtitle_rect = subtitle_image.get_rect(
            midtop=(settings.WIDTH // 2, title_rect.bottom + 8)
        )
        screen.blit(subtitle_image, subtitle_rect)
        content_top = max(panel.y + 116, subtitle_rect.bottom + 12)
        about_bottom = self._draw_wrapped_section(
            screen,
            "ABOUT",
            str(profile["fact"]),
            panel.x + 34,
            content_top,
            panel.width - 68,
        )
        impact_y = about_bottom + 10
        self._draw_wrapped_section(
            screen,
            "ENVIRONMENTAL IMPACT",
            str(profile["impact"]),
            panel.x + 34,
            impact_y,
            panel.width - 68,
            (210, 241, 229),
        )
        source_y = panel.y + 394
        source_image = self._fit_surface(
            self.small_font,
            f'Source: {profile["source_label"]}  [open]',
            (255, 221, 153),
            panel.width - 60,
        )
        self.source_link_rect = source_image.get_rect(center=(settings.WIDTH // 2, source_y))
        screen.blit(source_image, self.source_link_rect)
        self._text(
            screen,
            self.small_font,
            "Click the source to open it  |  Press F or ESC to close",
            settings.WHITE,
            (settings.WIDTH // 2, panel.y + 449),
        )
        return self.source_link_rect

    @staticmethod
    def _fit_surface(
        font: pygame.font.Font,
        text: str,
        color: tuple[int, int, int],
        max_width: int,
    ) -> pygame.Surface:
        """Reduce a single-line label's font until it fits its allocated width."""
        font_path = pygame.font.match_font(
            "Avenir Next",
            bold=font.get_bold(),
            italic=font.get_italic(),
        )
        size = max(12, font.size("M")[1])
        fitted_font = pygame.font.Font(font_path, size)
        while fitted_font.size(text)[0] > max_width and size > 12:
            size -= 1
            fitted_font = pygame.font.Font(font_path, size)
        return fitted_font.render(text, True, color)

    @classmethod
    def _fit_text(
        cls,
        screen: pygame.Surface,
        font: pygame.font.Font,
        text: str,
        color: tuple[int, int, int],
        center: tuple[int, int],
        max_width: int,
    ) -> pygame.Rect:
        image = cls._fit_surface(font, text, color, max_width)
        rect = image.get_rect(center=center)
        screen.blit(image, rect)
        return rect

    @staticmethod
    def _draw_pollutant_art(
        screen: pygame.Surface,
        illustration: str,
        center: tuple[int, int],
    ) -> None:
        """Draw a clear, enlarged version of the matching pollutant illustration."""
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

    def _draw_wrapped_section(
        self,
        screen: pygame.Surface,
        heading: str,
        text: str,
        left: int,
        top: int,
        max_width: int,
        color: tuple[int, int, int] = settings.WHITE,
    ) -> int:
        heading_image = self.small_font.render(heading, True, (255, 220, 150))
        screen.blit(heading_image, (left, top))
        lines: list[str] = []
        line = ""
        for word in text.split():
            candidate = f"{line} {word}".strip()
            if self.small_font.size(candidate)[0] > max_width and line:
                lines.append(line)
                line = word
            else:
                line = candidate
        if line:
            lines.append(line)
        line_height = self.small_font.get_linesize()
        text_top = top + heading_image.get_height() + 4
        for index, content in enumerate(lines[:3]):
            screen.blit(
                self.small_font.render(content, True, color),
                (left, text_top + index * line_height),
            )
        return text_top + min(3, len(lines)) * line_height

    def draw_result(
        self,
        screen: pygame.Surface,
        victory: bool,
        score: int,
        region_id: str = "gulf",
    ) -> None:
        overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)
        overlay.fill((4, 25, 49, 155))
        screen.blit(overlay, (0, 0))
        normalized_region = normalize_region_id(region_id)
        title = {
            "gulf": "REEF RESTORED!",
            "mediterranean": "MEADOW RESTORED!",
            "arctic": "HABITAT RESTORED!",
            "great_lakes": "HABITAT RESTORED!",
            "amazon": "RIVER RESTORED!",
        }[normalized_region] if victory else "DIVE OVER"
        habitat = {
            "gulf": "reef",
            "mediterranean": "seagrass meadow",
            "arctic": "Arctic habitat",
            "great_lakes": "freshwater habitat",
            "amazon": "river habitat",
        }[normalized_region]
        subtitle = (
            f"Your care helped the {habitat} recover."
            if victory
            else f"The {habitat} still needs you. Take a breath and try again."
        )
        self._text(screen, self.heading_font, title, settings.WHITE, (settings.WIDTH // 2, 280))
        self._text(screen, self.body_font, subtitle, settings.PALE_AQUA, (settings.WIDTH // 2, 339))
        self._text(screen, self.body_font, f"Pollution collected: {score}", settings.WHITE, (settings.WIDTH // 2, 394))
        self._text(screen, self.small_font, "Press ENTER or R to play again  |  ESC for menu", settings.WHITE, (settings.WIDTH // 2, 454))
