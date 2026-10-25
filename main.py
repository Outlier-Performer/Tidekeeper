"""Main entry point and game-state loop for Tidekeeper."""

import math
import random
import subprocess
import sys
import webbrowser
from pathlib import Path

import pygame

import settings
from audio import Audio
from camera import Camera
from enemies import Jellyfish
from items import PollutionField
from ocean import Ocean
from player import Player
from region_data import (
    REGION_HAZARD_PROFILE_IDS,
    REGION_IDS,
    REGION_LABELS,
    REGION_POLLUTION_PROFILES,
    normalize_region_id,
)
from ui import GameUI
from wildlife import WildlifeSystem
from world import depth_at, zone_at


MENU = "menu"
PLAYING = "playing"
VICTORY = "victory"
GAME_OVER = "game_over"
EXPLORE_MODE = "explore"
REGION_SELECT = "region_select"
ACTIVITY_SELECT = "activity_select"


class TidekeeperGame:
    def __init__(self) -> None:
        self.audio = Audio()
        pygame.init()
        pygame.display.set_caption(settings.TITLE)
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.clock = pygame.time.Clock()
        self.region_id = "gulf"
        self.ocean = Ocean(self.region_id)
        self.player = Player(region_id=self.region_id)
        self.camera = Camera()
        self.camera.update((self.player.x, self.player.y), 1.0)
        self.pollution = PollutionField(initial_item_count=4, region_id=self.region_id)
        self.ui = GameUI()
        self.wildlife = WildlifeSystem(self.region_id)
        self.random = random.Random()
        self.enemies: list[Jellyfish] = []
        self.state = MENU
        self.menu_step = REGION_SELECT
        self.mode = EXPLORE_MODE
        self.score = 0
        self.time_left = settings.GAME_TIME_SECONDS
        self.reef_health = 0.0
        self.current_zone = zone_at(self.player.y, self.region_id)
        self.zone_toast_timer = 0.0
        self.play_process: subprocess.Popen[bytes] | None = None
        self.poi_hitboxes: list[tuple[pygame.Rect, dict[str, object]]] = []
        self.was_boosting = False
        self._create_enemies()
        self.audio.play_music("explore")

    def _play_window_running(self) -> bool:
        return self.play_process is not None and self.play_process.poll() is None

    def _launch_play_window(self) -> None:
        """Open the compact mission as its own desktop window and process."""
        if self._play_window_running():
            return
        self.audio.play("click")
        play_script = Path(__file__).with_name("play_window.py")
        self.play_process = subprocess.Popen(
            [sys.executable, str(play_script), self.region_id],
            cwd=play_script.parent,
        )

    def select_region(self, region_id: str) -> None:
        self.region_id = normalize_region_id(region_id)
        self.ocean = Ocean(self.region_id)
        self.player = Player(region_id=self.region_id)
        self.camera = Camera()
        self.camera.update((self.player.x, self.player.y), 1.0)
        self.pollution = PollutionField(
            initial_item_count=4,
            region_id=self.region_id,
        )
        self.wildlife = WildlifeSystem(self.region_id)
        self.current_zone = zone_at(self.player.y, self.region_id)
        self.menu_step = ACTIVITY_SELECT
        self._create_enemies()
        self.audio.play("click")

    def _open_info(self, profile: dict[str, object]) -> None:
        self.wildlife.open_info(profile)
        self.audio.play("card")

    def _close_info(self) -> None:
        self.wildlife.close_card()
        self.audio.play("click")

    def _return_to_menu(self, menu_step: str) -> None:
        self.state = MENU
        self.menu_step = menu_step
        self.audio.play("click")

    def _create_enemies(self) -> None:
        self.enemies = []
        for index in range(settings.JELLYFISH_COUNT):
            if index < (4 if self.region_id == "gulf" else 3):
                x = self.random.randint(170, 900)
                y = self.random.randint(280, 820)
            else:
                x = self.random.randint(100, settings.WORLD_WIDTH - 100)
                y = self.random.randint(settings.HUD_HEIGHT + 100, settings.WORLD_HEIGHT - 100)
            self.enemies.append(
                Jellyfish(
                    x,
                    y,
                    phase=index * 1.7,
                    speed=self.random.uniform(0.8, 1.25),
                    region_id=self.region_id,
                )
            )

    def start_game(self, region_id: str | None = None) -> None:
        if region_id is not None and region_id != self.region_id:
            self.select_region(region_id)
        self.player.reset()
        self.camera.update((self.player.x, self.player.y), 1.0)
        self.pollution.reset((self.player.x, self.player.y))
        self.wildlife.reset()
        self.score = 0
        self.time_left = settings.GAME_TIME_SECONDS
        self.reef_health = 0.0
        self.ocean.set_reef_health(self.reef_health)
        self.mode = EXPLORE_MODE
        self.current_zone = zone_at(self.player.y, self.region_id)
        self.zone_toast_timer = 0.0
        self._create_enemies()
        self.state = PLAYING
        self.audio.play("click")

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.audio.toggle_mute()
                elif self.state == MENU:
                    if self.menu_step == REGION_SELECT:
                        region_index = event.key - pygame.K_1
                        if 0 <= region_index < len(REGION_IDS):
                            self.select_region(REGION_IDS[region_index])
                    elif event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                        self._return_to_menu(REGION_SELECT)
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_e):
                        self.start_game()
                    elif event.key == pygame.K_p:
                        self._launch_play_window()
                elif self.state in (VICTORY, GAME_OVER):
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_r):
                        self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self._return_to_menu(ACTIVITY_SELECT)
                elif self.state == PLAYING:
                    if self.wildlife.open_profile is not None and event.key in (pygame.K_f, pygame.K_ESCAPE):
                        self._close_info()
                    elif event.key == pygame.K_f and self.mode == EXPLORE_MODE:
                        profile = self._nearby_info_profile()
                        if profile is not None:
                            self._open_info(profile)
                    elif event.key == pygame.K_ESCAPE:
                        self._return_to_menu(ACTIVITY_SELECT)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.state == MENU:
                if self.menu_step == REGION_SELECT:
                    for region_id, rect in self.ui.region_button_rects.items():
                        if rect.collidepoint(event.pos):
                            self.select_region(region_id)
                            break
                elif self.ui.explore_button_rect.collidepoint(event.pos):
                    self.start_game()
                elif self.ui.play_button_rect.collidepoint(event.pos):
                    self._launch_play_window()
                elif self.ui.back_button_rect.collidepoint(event.pos):
                    self._return_to_menu(REGION_SELECT)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.state == PLAYING:
                if self.wildlife.open_profile is not None:
                    if (
                        self.ui.photo_link_rect is not None
                        and self.ui.photo_link_rect.collidepoint(event.pos)
                        and self.ui.photo_link_url is not None
                    ):
                        webbrowser.open(self.ui.photo_link_url)
                    elif (
                        self.ui.source_link_rect is not None
                        and self.ui.source_link_rect.collidepoint(event.pos)
                    ):
                        webbrowser.open(str(self.wildlife.open_profile["source"]))
                    else:
                        self._close_info()
                elif self.mode == EXPLORE_MODE:
                    profile = self._profile_clicked(event.pos)
                    if profile is not None:
                        self._open_info(profile)
        return True

    def update(self, dt: float) -> None:
        # The Play window has its own soundtrack, so hold ours while it is open.
        self.audio.set_music_paused(self._play_window_running())
        self.wildlife.update(dt)
        if self.state != PLAYING:
            self.ocean.update(dt, self.camera)
            return

        card_open = self.wildlife.open_profile is not None
        if not card_open:
            self.player.update(dt, pygame.key.get_pressed())
            self.camera.update((self.player.x, self.player.y), dt)
            if self.player.boosting and not self.was_boosting:
                self.audio.play("boost")
            self.was_boosting = self.player.boosting

        self.ocean.update(dt, self.camera)
        for enemy in self.enemies:
            if self.camera.sees((enemy.x, enemy.y), 180):
                enemy.update(dt)
        self.pollution.update(dt, (self.player.x, self.player.y))

        zone = zone_at(self.player.y, self.region_id)
        if zone.key != self.current_zone.key:
            self.current_zone = zone
            self.zone_toast_timer = 2.8
            self.audio.play("zone")
        else:
            self.zone_toast_timer = max(0.0, self.zone_toast_timer - dt)

    def draw(self) -> None:
        self.poi_hitboxes = []
        self.ocean.draw(self.screen, self.camera)
        if self.state == MENU:
            if self.menu_step == REGION_SELECT:
                self.ui.draw_region_select(self.screen, pygame.mouse.get_pos())
            else:
                self.ui.draw_activity_select(
                    self.screen,
                    pygame.mouse.get_pos(),
                    self.region_id,
                )
        else:
            self.poi_hitboxes.extend(self.ocean.info_hitboxes(self.camera))
            self.pollution.draw(self.screen, self.camera)
            hazard_profile = self.wildlife.profile_for(
                REGION_HAZARD_PROFILE_IDS[self.region_id]
            )
            for enemy in self.enemies:
                enemy.draw(self.screen, self.camera)
                if self.camera.sees((enemy.x, enemy.y), 60):
                    x, y = self.camera.world_to_screen((enemy.x, enemy.y))
                    self.poi_hitboxes.append(
                        (pygame.Rect(x - 28, y - 36, 56, 72), hazard_profile)
                    )
            self.wildlife.draw(self.screen, self.camera, self.ocean.time, self.poi_hitboxes)
            pollution_profiles = REGION_POLLUTION_PROFILES[self.region_id]
            for item in self.pollution.items:
                if self.camera.sees((item.x, item.y), 30):
                    screen_x, screen_y = self.camera.world_to_screen((item.x, item.y))
                    hitbox = pygame.Rect(screen_x - 19, screen_y - 19, 38, 38)
                    profile = pollution_profiles.get(item.kind)
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
                    region_title=REGION_LABELS[self.region_id],
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
                self.ui.draw_result(
                    self.screen,
                    self.state == VICTORY,
                    self.score,
                    self.region_id,
                )

        pygame.display.flip()

    def _profile_clicked(self, screen_position: tuple[int, int]) -> dict[str, object] | None:
        """Use what was actually drawn so clicks match visible artwork."""
        if self._player_screen_rect().collidepoint(screen_position):
            return None
        for hitbox, profile in reversed(self.poi_hitboxes):
            if hitbox.collidepoint(screen_position):
                return profile
        return None

    def _player_screen_rect(self) -> pygame.Rect:
        screen_x, screen_y = self.camera.world_to_screen(
            (self.player.x, self.player.y)
        )
        return pygame.Rect(screen_x - 42, screen_y - 29, 84, 58)

    def _nearby_info_profile(self) -> dict[str, object] | None:
        """Find the nearest visible information target within interaction range."""
        player_rect = self._player_screen_rect()
        player_screen = player_rect.center
        nearest_profile = None
        nearest_key: tuple[int, float] | None = None
        for hitbox, profile in reversed(self.poi_hitboxes):
            if hitbox.colliderect(player_rect):
                distance = math.hypot(
                    player_screen[0] - hitbox.centerx,
                    player_screen[1] - hitbox.centery,
                )
                selection_key = (0, distance)
            else:
                closest_x = max(hitbox.left, min(player_screen[0], hitbox.right))
                closest_y = max(hitbox.top, min(player_screen[1], hitbox.bottom))
                distance = math.hypot(
                    player_screen[0] - closest_x,
                    player_screen[1] - closest_y,
                )
                if distance > settings.WILDLIFE_OBSERVE_RADIUS:
                    continue
                selection_key = (1, distance)

            if nearest_key is None or selection_key < nearest_key:
                nearest_profile = profile
                nearest_key = selection_key
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
