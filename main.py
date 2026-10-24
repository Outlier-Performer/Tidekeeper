"""Main entry point and game-state loop for Tidekeeper."""

import random

import pygame

import settings
from enemies import Jellyfish
from items import PollutionField
from ocean import Ocean
from player import Player
from ui import GameUI


MENU = "menu"
PLAYING = "playing"
VICTORY = "victory"
GAME_OVER = "game_over"


class TidekeeperGame:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(settings.TITLE)
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.clock = pygame.time.Clock()
        self.ocean = Ocean()
        self.player = Player()
        self.pollution = PollutionField()
        self.ui = GameUI()
        self.random = random.Random()
        self.enemies: list[Jellyfish] = []
        self.state = MENU
        self.score = 0
        self.time_left = settings.GAME_TIME_SECONDS
        self.reef_health = 0.0
        self._create_enemies()

    def _create_enemies(self) -> None:
        self.enemies = []
        for index in range(settings.JELLYFISH_COUNT):
            x = self.random.randint(105, settings.WIDTH - 105)
            y = self.random.randint(settings.HUD_HEIGHT + 100, settings.OCEAN_FLOOR_Y - 100)
            self.enemies.append(Jellyfish(x, y, phase=index * 1.7, speed=self.random.uniform(0.8, 1.25)))

    def start_game(self) -> None:
        self.player.reset()
        self.pollution.reset()
        self.score = 0
        self.time_left = settings.GAME_TIME_SECONDS
        self.reef_health = 0.0
        self.ocean.set_reef_health(self.reef_health)
        self._create_enemies()
        self.state = PLAYING

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if self.state == MENU and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    self.start_game()
                elif self.state in (VICTORY, GAME_OVER):
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_r):
                        self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = MENU
                elif self.state == PLAYING and event.key == pygame.K_ESCAPE:
                    self.state = MENU
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.state == MENU:
                if self.ui.start_button_rect.collidepoint(event.pos):
                    self.start_game()
        return True

    def update(self, dt: float) -> None:
        self.ocean.update(dt)
        if self.state != PLAYING:
            return

        self.time_left -= dt
        self.player.update(dt, pygame.key.get_pressed())
        self.pollution.update(dt)
        for enemy in self.enemies:
            enemy.update(dt)

        collected = self.pollution.collect_collisions(self.player.rect)
        self.score = min(settings.TARGET_SCORE, self.score + len(collected) * settings.POLLUTION_SCORE)
        self.reef_health = min(1.0, self.score * settings.POLLUTION_REEF_GAIN)
        self.ocean.set_reef_health(self.reef_health)

        for enemy in self.enemies:
            if enemy.rect.colliderect(self.player.rect):
                self.player.take_damage()

        if self.score >= settings.TARGET_SCORE:
            self.state = VICTORY
        elif self.player.health <= 0 or self.time_left <= 0:
            self.state = GAME_OVER

    def draw(self) -> None:
        self.ocean.draw(self.screen)
        if self.state == MENU:
            self.ui.draw_menu(self.screen, pygame.mouse.get_pos())
        else:
            for item in self.pollution.items:
                item.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw(self.screen)
            self.player.draw(self.screen)
            for effect in self.pollution.effects:
                effect.draw(self.screen)

            if self.state == PLAYING:
                self.ui.draw_hud(self.screen, self.player.health, self.score, self.reef_health, self.time_left)
            else:
                self.ui.draw_result(self.screen, self.state == VICTORY, self.score)

        pygame.display.flip()

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
