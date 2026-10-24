"""Menu, fixed HUD, and source-linked point-of-interest cards."""

import pygame

import settings
from wildlife import WildlifeSystem


class GameUI:
    def __init__(self) -> None:
        self.title_font = pygame.font.SysFont("Avenir Next", 62, bold=True)
        self.heading_font = pygame.font.SysFont("Avenir Next", 37, bold=True)
        self.body_font = pygame.font.SysFont("Avenir Next", 22)
        self.small_font = pygame.font.SysFont("Avenir Next", 18)
        self.explore_button_rect = pygame.Rect(settings.WIDTH // 2 - 235, 423, 220, 60)
        self.play_button_rect = pygame.Rect(settings.WIDTH // 2 + 15, 423, 220, 60)
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

    def draw_menu(self, screen: pygame.Surface, mouse_position: tuple[int, int]) -> None:
        panel = pygame.Surface((860, 430), pygame.SRCALPHA)
        pygame.draw.rect(panel, (3, 29, 50, 200), panel.get_rect(), border_radius=26)
        pygame.draw.rect(panel, (103, 211, 204, 90), panel.get_rect(), 1, border_radius=26)
        screen.blit(panel, (70, 155))
        self._text(screen, self.title_font, "TIDEKEEPER", settings.WHITE, (settings.WIDTH // 2, 225))
        self._text(screen, self.body_font, "Explore a stylized Gulf of Mexico underwater world.", settings.PALE_AQUA, (settings.WIDTH // 2, 295))
        explore_color = (255, 185, 117) if self.explore_button_rect.collidepoint(mouse_position) else (255, 158, 104)
        play_color = (132, 222, 204) if self.play_button_rect.collidepoint(mouse_position) else (96, 193, 183)
        pygame.draw.rect(screen, explore_color, self.explore_button_rect, border_radius=17)
        pygame.draw.rect(screen, play_color, self.play_button_rect, border_radius=17)
        self._fit_text(
            screen,
            self.body_font,
            "EXPLORE WORLD",
            settings.INK,
            self.explore_button_rect.center,
            self.explore_button_rect.width - 20,
        )
        self._fit_text(
            screen,
            self.body_font,
            "OPEN PLAY WINDOW",
            settings.INK,
            self.play_button_rect.center,
            self.play_button_rect.width - 20,
        )
        self._text(screen, self.small_font, "Swim: WASD / arrows  |  Boost: hold SHIFT  |  Inspect: press F", settings.PALE_AQUA, (settings.WIDTH // 2, 538))
        self._text(screen, self.small_font, "Click OPEN PLAY WINDOW to start cleanup: collect litter and avoid predators.", settings.WHITE, (settings.WIDTH // 2, 567))

    def draw_difficulty_select(
        self,
        screen: pygame.Surface,
        mouse_position: tuple[int, int],
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
        descriptions = {
            "easy": ("EASY", "10 pieces  |  6 jellyfish"),
            "medium": ("MEDIUM", "15 pieces  |  9 jellyfish"),
            "hard": ("HARD", "20 pieces  |  12 jellyfish"),
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
            "Sharks get faster and notice you from farther away on harder settings.",
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
    ) -> None:
        pygame.draw.rect(screen, (4, 38, 65), (0, 0, settings.WIDTH, settings.HUD_HEIGHT))
        pygame.draw.line(screen, (84, 198, 193), (0, settings.HUD_HEIGHT - 2), (settings.WIDTH, settings.HUD_HEIGHT - 2), 2)
        mode_label = "EXPLORE WORLD" if mode == "explore" else "CLEANUP MISSION"
        self._text(screen, self.small_font, mode_label, settings.WHITE, (109, 20))
        timer_label = f"TIME {max(0, int(time_left + 0.999)):03d}s" if mode == "play" else "TIME PAUSED"
        self._text(screen, self.small_font, timer_label, settings.WHITE, (902, 20))
        self._text(screen, self.small_font, f"{habitat}  |  approx. {depth}m game depth", settings.PALE_AQUA, (420, 55))
        self._text(screen, self.small_font, f"FIELD NOTES {discoveries}", settings.WHITE, (834, 55))
        if mode == "explore":
            self._text(screen, self.small_font, "OPEN PLAY WINDOW", settings.PALE_AQUA, (131, 74))
            self._text(screen, self.small_font, "CLICK TO LEARN  |  Inspect: press F", settings.WHITE, (370, 20))
            self._draw_boost_bar(screen, boost_energy)
            return

        self._text(screen, self.small_font, "HEALTH", settings.PALE_AQUA, (66, 74))
        for index in range(settings.PLAYER_STARTING_HEALTH):
            color = settings.HEART_RED if index < health else (88, 111, 122)
            self._draw_heart(screen, 114 + index * 27, 72, color)
        target = settings.TARGET_SCORE if target_score is None else target_score
        self._text(screen, self.small_font, f"CLEANED {score}/{target}", settings.WHITE, (260, 74))
        self._text(screen, self.small_font, "REEF", settings.PALE_AQUA, (394, 74))
        bar = pygame.Rect(424, 66, 125, 16)
        pygame.draw.rect(screen, (24, 74, 89), bar, border_radius=8)
        fill = bar.copy()
        fill.width = round(bar.width * max(0.0, min(1.0, reef_health)))
        if fill.width:
            pygame.draw.rect(screen, (86, 222, 177), fill, border_radius=8)
        pygame.draw.rect(screen, (118, 211, 202), bar, 2, border_radius=8)
        self._draw_boost_bar(screen, boost_energy)

    def _draw_boost_bar(self, screen: pygame.Surface, energy: float) -> None:
        self._text(screen, self.small_font, "BOOST", settings.PALE_AQUA, (604, 74))
        bar = pygame.Rect(645, 66, 122, 16)
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
            self._draw_pollutant_art(screen, str(profile.get("illustration", "")), (panel.centerx, panel.y + 132))
            content_top = panel.y + 176
        else:
            content_top = panel.y + 116
            WildlifeSystem.draw_card_illustration(
                screen,
                profile,
                (panel.x + 59, panel.y + 56),
            )

        self._fit_text(
            screen,
            self.heading_font,
            str(profile["name"]),
            settings.WHITE,
            (settings.WIDTH // 2 + (35 if not is_pollutant else 0), panel.y + 48),
            panel.width - (112 if not is_pollutant else 50),
        )
        self._fit_text(
            screen,
            self.small_font,
            f'{str(profile["kind"]).upper()}  |  {profile["habitat"]}',
            settings.PALE_AQUA,
            (settings.WIDTH // 2, panel.y + 86),
            panel.width - 60,
        )
        if is_pollutant:
            about_y = content_top
            impact_y = panel.y + 266
            source_y = panel.y + 394
        else:
            about_y = content_top
            impact_y = content_top + 91
            source_y = panel.y + 394
        self._draw_wrapped_section(
            screen, "ABOUT", str(profile["fact"]), panel.x + 34, about_y, panel.width - 68
        )
        self._draw_wrapped_section(
            screen,
            "ENVIRONMENTAL IMPACT",
            str(profile["impact"]),
            panel.x + 34,
            impact_y,
            panel.width - 68,
            (210, 241, 229),
        )
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
    ) -> None:
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
        for index, content in enumerate(lines[:3]):
            screen.blit(self.small_font.render(content, True, color), (left, top + 24 + index * 21))

    def draw_result(self, screen: pygame.Surface, victory: bool, score: int) -> None:
        overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)
        overlay.fill((4, 25, 49, 155))
        screen.blit(overlay, (0, 0))
        title = "REEF RESTORED!" if victory else "DIVE OVER"
        subtitle = "Your care brought the reef back to life." if victory else "The reef still needs you. Take a breath and try again."
        self._text(screen, self.heading_font, title, settings.WHITE, (settings.WIDTH // 2, 280))
        self._text(screen, self.body_font, subtitle, settings.PALE_AQUA, (settings.WIDTH // 2, 339))
        self._text(screen, self.body_font, f"Pollution collected: {score}", settings.WHITE, (settings.WIDTH // 2, 394))
        self._text(screen, self.small_font, "Press ENTER or R to play again  |  ESC for menu", settings.WHITE, (settings.WIDTH // 2, 454))
