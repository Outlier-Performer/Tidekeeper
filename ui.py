"""Menu, HUD, and result screens."""

import pygame

import settings


class GameUI:
    def __init__(self) -> None:
        self.title_font = pygame.font.SysFont("Avenir Next", 62, bold=True)
        self.heading_font = pygame.font.SysFont("Avenir Next", 42, bold=True)
        self.body_font = pygame.font.SysFont("Avenir Next", 24)
        self.small_font = pygame.font.SysFont("Avenir Next", 18)
        self.start_button_rect = pygame.Rect(settings.WIDTH // 2 - 112, 423, 224, 60)

    @staticmethod
    def _text(
        screen: pygame.Surface,
        font: pygame.font.Font,
        text: str,
        color: tuple[int, int, int],
        center: tuple[int, int],
    ) -> None:
        image = font.render(text, True, color)
        screen.blit(image, image.get_rect(center=center))

    def draw_menu(self, screen: pygame.Surface, mouse_position: tuple[int, int]) -> None:
        self._text(screen, self.title_font, "TIDEKEEPER", settings.WHITE, (settings.WIDTH // 2, 225))
        self._text(screen, self.body_font, "A little care can bring a whole reef back to life.", settings.PALE_AQUA, (settings.WIDTH // 2, 295))
        hovered = self.start_button_rect.collidepoint(mouse_position)
        button_color = (255, 185, 117) if hovered else (255, 158, 104)
        pygame.draw.rect(screen, button_color, self.start_button_rect, border_radius=17)
        self._text(screen, self.body_font, "START EXPLORING", settings.INK, self.start_button_rect.center)
        self._text(screen, self.small_font, "Press ENTER  |  Swim: WASD / arrows  |  Boost: SPACE", settings.WHITE, (settings.WIDTH // 2, 516))

    def draw_hud(self, screen: pygame.Surface, health: int, score: int, reef_health: float, time_left: float) -> None:
        pygame.draw.rect(screen, (4, 38, 65), (0, 0, settings.WIDTH, settings.HUD_HEIGHT))
        pygame.draw.line(screen, (84, 198, 193), (0, settings.HUD_HEIGHT - 2), (settings.WIDTH, settings.HUD_HEIGHT - 2), 2)

        self._text(screen, self.body_font, "HEALTH", settings.PALE_AQUA, (88, 27))
        for index in range(settings.PLAYER_STARTING_HEALTH):
            color = settings.HEART_RED if index < health else (88, 111, 122)
            self._draw_heart(screen, 48 + index * 34, 57, color)

        self._text(screen, self.body_font, f"CLEANED  {score}/{settings.TARGET_SCORE}", settings.WHITE, (288, 43))
        self._text(screen, self.small_font, "REEF", settings.PALE_AQUA, (493, 26))
        bar = pygame.Rect(540, 17, 190, 19)
        pygame.draw.rect(screen, (24, 74, 89), bar, border_radius=9)
        fill = bar.copy()
        fill.width = round(bar.width * max(0.0, min(1.0, reef_health)))
        if fill.width:
            pygame.draw.rect(screen, (86, 222, 177), fill, border_radius=9)
        pygame.draw.rect(screen, (118, 211, 202), bar, 2, border_radius=9)

        self._text(screen, self.body_font, f"{max(0, int(time_left + 0.999)):03d}s", settings.WHITE, (883, 42))
        self._text(screen, self.small_font, "SPACE  BOOST", settings.PALE_AQUA, (settings.WIDTH - 95, 68))

    def _draw_heart(self, screen: pygame.Surface, x: int, y: int, color: tuple[int, int, int]) -> None:
        pygame.draw.circle(screen, color, (x - 5, y - 4), 7)
        pygame.draw.circle(screen, color, (x + 5, y - 4), 7)
        pygame.draw.polygon(screen, color, [(x - 12, y - 1), (x + 12, y - 1), (x, y + 13)])

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
