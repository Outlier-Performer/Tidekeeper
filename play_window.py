"""Standalone compact cleanup-mission window launched from Explore Mode."""

import pygame

import settings
from camera import Camera
from enemies import Shark
from items import PollutionField
from ocean import Ocean
from player import Player
from ui import GameUI
from world import depth_at, zone_at


ARENA_BOUNDS = (1450, 1000, 2550, 1800)
ARENA_START = (2000.0, 1400.0)


class CleanupGame:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Tidekeeper - Gulf Cleanup Mission")
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.clock = pygame.time.Clock()
        self.camera = Camera()
        self.player = Player(world_bounds=ARENA_BOUNDS, start_position=ARENA_START)
        self.ocean = Ocean()
        self.items = PollutionField(world_bounds=ARENA_BOUNDS)
        self.ui = GameUI()
        self.camera.update(ARENA_START, 1.0)
        self.sharks: list[Shark] = []
        self.score = 0
        self.time_left = settings.GAME_TIME_SECONDS
        self.reef_health = 0.0
        self.state = "playing"
        self.zone = zone_at(self.player.y)
        self.reset()

    def reset(self) -> None:
        self.player.reset()
        self.camera.update(ARENA_START, 1.0)
        self.items.reset(ARENA_START)
        self.score = 0
        self.time_left = settings.GAME_TIME_SECONDS
        self.reef_health = 0.0
        self.ocean.set_reef_health(0.0)
        self.state = "playing"
        self.sharks = [
            Shark(1590, 1170, 83),
            Shark(2380, 1110, 94),
            Shark(1615, 1670, 77),
        ]

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if self.state in ("victory", "game_over") and event.key in (
                    pygame.K_RETURN,
                    pygame.K_KP_ENTER,
                    pygame.K_r,
                ):
                    self.reset()
        return True

    def update(self, dt: float) -> None:
        if self.state != "playing":
            self.ocean.update(dt, self.camera)
            return

        self.player.update(dt, pygame.key.get_pressed())
        self.camera.update((self.player.x, self.player.y), dt)
        self.ocean.update(dt, self.camera)
        self.items.update(dt, (self.player.x, self.player.y))
        self.time_left -= dt
        self.zone = zone_at(self.player.y)

        target = (self.player.x, self.player.y)
        for shark in self.sharks:
            if self.camera.sees((shark.x, shark.y), 200):
                shark.update(dt, target)

        collected = self.items.collect_collisions(self.player.rect)
        self.score = min(
            settings.TARGET_SCORE,
            self.score + len(collected) * settings.POLLUTION_SCORE,
        )
        self.reef_health = min(1.0, self.score * settings.POLLUTION_REEF_GAIN)
        self.ocean.set_reef_health(self.reef_health)

        for shark in self.sharks:
            if shark.rect.colliderect(self.player.rect):
                self.player.take_damage()

        if self.score >= settings.TARGET_SCORE:
            self.state = "victory"
        elif self.player.health <= 0 or self.time_left <= 0:
            self.state = "game_over"

    def draw(self) -> None:
        self.ocean.draw(self.screen, self.camera)
        self.items.draw(self.screen, self.camera)
        for shark in self.sharks:
            shark.draw(self.screen, self.camera)
        self.player.draw(self.screen, self.camera)

        if self.state == "playing":
            self.ui.draw_hud(
                self.screen,
                self.player.health,
                self.score,
                self.reef_health,
                self.time_left,
                "play",
                self.zone.name,
                depth_at(self.player.y),
                0,
            )
        else:
            self.ui.draw_result(self.screen, self.state == "victory", self.score)

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
    CleanupGame().run()


if __name__ == "__main__":
    main()
