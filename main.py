"""Main entry point and game-state loop for Tidekeeper."""

import random
import subprocess
import sys
import webbrowser
from pathlib import Path

import pygame

from ecology_data import POLLUTION_PROFILES
import settings
from camera import Camera
from enemies import Jellyfish
from items import PollutionField
from ocean import Ocean
from player import Player
from ui import GameUI
from wildlife import WildlifeSystem
from world import depth_at, zone_at


MENU = "menu"
PLAYING = "playing"
VICTORY = "victory"
GAME_OVER = "game_over"
EXPLORE_MODE = "explore"


class TidekeeperGame:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(settings.TITLE)
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.clock = pygame.time.Clock()
        self.ocean = Ocean()
        self.player = Player()
        self.camera = Camera()
        self.camera.update((self.player.x, self.player.y), 1.0)
        self.pollution = PollutionField(initial_item_count=4)
        self.ui = GameUI()
        self.wildlife = WildlifeSystem()
        self.random = random.Random()
        self.enemies: list[Jellyfish] = []
        self.state = MENU
        self.mode = EXPLORE_MODE
        self.score = 0
        self.time_left = settings.GAME_TIME_SECONDS
        self.reef_health = 0.0
        self.current_zone = zone_at(self.player.y)
        self.zone_toast_timer = 0.0
        self.play_process: subprocess.Popen[bytes] | None = None
        self.poi_hitboxes: list[tuple[pygame.Rect, dict[str, object]]] = []
        self._create_enemies()

    def _launch_play_window(self) -> None:
        """Open the compact mission as its own desktop window and process."""
        if self.play_process is not None and self.play_process.poll() is None:
            return
        play_script = Path(__file__).with_name("play_window.py")
        self.play_process = subprocess.Popen(
            [sys.executable, str(play_script)],
            cwd=play_script.parent,
        )

    def _create_enemies(self) -> None:
        self.enemies = []
        for index in range(settings.JELLYFISH_COUNT):
            if index < 4:
                x = self.random.randint(170, 900)
                y = self.random.randint(280, 820)
            else:
                x = self.random.randint(100, settings.WORLD_WIDTH - 100)
                y = self.random.randint(settings.HUD_HEIGHT + 100, settings.WORLD_HEIGHT - 100)
            self.enemies.append(
                Jellyfish(x, y, phase=index * 1.7, speed=self.random.uniform(0.8, 1.25))
            )

    def start_game(self) -> None:
        self.player.reset()
        self.camera.update((self.player.x, self.player.y), 1.0)
        self.pollution.reset((self.player.x, self.player.y))
        self.wildlife.reset()
        self.score = 0
        self.time_left = settings.GAME_TIME_SECONDS
        self.reef_health = 0.0
        self.ocean.set_reef_health(self.reef_health)
        self.mode = EXPLORE_MODE
        self.current_zone = zone_at(self.player.y)
        self.zone_toast_timer = 0.0
        self._create_enemies()
        self.state = PLAYING

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if self.state == MENU:
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_e):
                        self.start_game()
                elif self.state in (VICTORY, GAME_OVER):
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_r):
                        self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = MENU
                elif self.state == PLAYING:
                    if self.wildlife.open_profile is not None and event.key in (pygame.K_f, pygame.K_ESCAPE):
                        self.wildlife.close_card()
                    elif event.key == pygame.K_f and self.mode == EXPLORE_MODE:
                        profile = self._nearby_info_profile()
                        if profile is not None:
                            self.wildlife.open_info(profile)
                    elif event.key == pygame.K_ESCAPE:
                        self.state = MENU
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.state == MENU:
                if self.ui.explore_button_rect.collidepoint(event.pos):
                    self.start_game()
                elif self.ui.play_button_rect.collidepoint(event.pos):
                    self._launch_play_window()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.state == PLAYING:
                if self.wildlife.open_profile is not None:
                    if (
                        self.ui.source_link_rect is not None
                        and self.ui.source_link_rect.collidepoint(event.pos)
                    ):
                        webbrowser.open(str(self.wildlife.open_profile["source"]))
                    else:
                        self.wildlife.close_card()
                elif self.mode == EXPLORE_MODE:
                    profile = self._profile_clicked(event.pos)
                    if profile is not None:
                        self.wildlife.open_info(profile)
        return True

    def update(self, dt: float) -> None:
        self.wildlife.update(dt)
        if self.state != PLAYING:
            self.ocean.update(dt, self.camera)
            return

        card_open = self.wildlife.open_profile is not None
        if not card_open:
            self.player.update(dt, pygame.key.get_pressed())
            self.camera.update((self.player.x, self.player.y), dt)

        self.ocean.update(dt, self.camera)
        for enemy in self.enemies:
            if self.camera.sees((enemy.x, enemy.y), 180):
                enemy.update(dt)
        self.pollution.update(dt, (self.player.x, self.player.y))

        zone = zone_at(self.player.y)
        if zone.key != self.current_zone.key:
            self.current_zone = zone
            self.zone_toast_timer = 2.8
        else:
            self.zone_toast_timer = max(0.0, self.zone_toast_timer - dt)

    def draw(self) -> None:
        self.poi_hitboxes = []
        self.ocean.draw(self.screen, self.camera)
        if self.state == MENU:
            self.ui.draw_menu(self.screen, pygame.mouse.get_pos())
        else:
            self.poi_hitboxes.extend(self.ocean.info_hitboxes(self.camera))
            self.pollution.draw(self.screen, self.camera)
            for enemy in self.enemies:
                enemy.draw(self.screen, self.camera)
                profile = self.wildlife.profile_for("moon_jellyfish")
                if self.camera.sees((enemy.x, enemy.y), 60):
                    x, y = self.camera.world_to_screen((enemy.x, enemy.y))
                    self.poi_hitboxes.append(
                        (pygame.Rect(x - 28, y - 36, 56, 72), profile)
                    )
            self.wildlife.draw(self.screen, self.camera, self.ocean.time, self.poi_hitboxes)
            for item in self.pollution.items:
                if self.camera.sees((item.x, item.y), 30):
                    screen_x, screen_y = self.camera.world_to_screen((item.x, item.y))
                    hitbox = pygame.Rect(screen_x - 19, screen_y - 19, 38, 38)
                    profile = POLLUTION_PROFILES.get(item.kind)
                    if profile is not None:
                        self.poi_hitboxes.append((hitbox, profile))
            self.player.draw(self.screen, self.camera)

            if self.state == PLAYING:
                self.ui.draw_hud(
                    self.screen,
                    self.player.health,
                    self.score,
                    self.reef_health,
                    self.time_left,
                    EXPLORE_MODE,
                    self.current_zone.name,
                    depth_at(self.player.y),
                    len(self.wildlife.discovered),
                    boost_energy=self.player.boost_energy,
                )
                if self.zone_toast_timer > 0:
                    self.ui.draw_zone_toast(self.screen, self.current_zone.name)
                if self.mode == EXPLORE_MODE:
                    self.wildlife.draw_prompt(
                        self.screen,
                        self._nearby_info_profile(),
                    )
                if self.wildlife.open_profile is not None:
                    self.ui.draw_discovery_card(
                        self.screen,
                        self.wildlife.open_profile,
                    )
            else:
                self.ui.draw_result(self.screen, self.state == VICTORY, self.score)

        pygame.display.flip()

    def _profile_clicked(self, screen_position: tuple[int, int]) -> dict[str, object] | None:
        """Use what was actually drawn so clicks match visible artwork."""
        for hitbox, profile in reversed(self.poi_hitboxes):
            if hitbox.collidepoint(screen_position):
                return profile
        return None

    def _nearby_info_profile(self) -> dict[str, object] | None:
        """Find the nearest visible information target within interaction range."""
        player_screen = self.camera.world_to_screen((self.player.x, self.player.y))
        nearest_profile = None
        nearest_distance = settings.WILDLIFE_OBSERVE_RADIUS
        for hitbox, profile in self.poi_hitboxes:
            closest_x = max(hitbox.left, min(player_screen[0], hitbox.right))
            closest_y = max(hitbox.top, min(player_screen[1], hitbox.bottom))
            distance = ((player_screen[0] - closest_x) ** 2 + (player_screen[1] - closest_y) ** 2) ** 0.5
            if distance <= nearest_distance:
                nearest_profile = profile
                nearest_distance = distance
        return nearest_profile

    def run(self) -> None:
        running = True
        while running:
            dt = min(self.clock.tick(settings.FPS) / 1000.0, 0.05)
            running = self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()


def main() -> None:
    TidekeeperGame().run()


if __name__ == "__main__":
    main()
