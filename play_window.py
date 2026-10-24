"""Standalone compact cleanup-mission window launched from Explore Mode."""

import random

import pygame

import settings
from camera import Camera
from enemies import Jellyfish, Shark
from items import PollutionField
from ocean import Ocean
from player import Player
from ui import GameUI
from world import depth_at, zone_at


ARENA_BOUNDS = (1100, 800, 2900, 2200)
ARENA_START = (2000.0, 1500.0)
DIFFICULTIES = {
    "easy": {
        "target_score": 10,
        "jellyfish_count": 6,
        "shark_speed_multiplier": 0.9,
        "shark_tracking_distance": 380,
    },
    "medium": {
        "target_score": 15,
        "jellyfish_count": 9,
        "shark_speed_multiplier": 1.0,
        "shark_tracking_distance": 440,
    },
    "hard": {
        "target_score": 20,
        "jellyfish_count": 12,
        "shark_speed_multiplier": 1.12,
        "shark_tracking_distance": 500,
    },
}


class CleanupGame:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Tidekeeper - Gulf Cleanup Mission")
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.clock = pygame.time.Clock()
        self.camera = Camera()
        self.player = Player(world_bounds=ARENA_BOUNDS, start_position=ARENA_START)
        self.ocean = Ocean()
        self.items = PollutionField(
            world_bounds=ARENA_BOUNDS,
            spawn_new_items=False,
            initial_item_count=DIFFICULTIES["easy"]["target_score"],
        )
        self.ui = GameUI()
        self.random = random.Random()
        self.camera.update(ARENA_START, 1.0)
        self.sharks: list[Shark] = []
        self.jellyfish: list[Jellyfish] = []
        self.score = 0
        self.time_left = settings.GAME_TIME_SECONDS
        self.reef_health = 0.0
        self.difficulty = "easy"
        self.state = "difficulty_select"
        self.zone = zone_at(self.player.y)

    def reset(self, difficulty: str | None = None) -> None:
        difficulty = difficulty or self.difficulty
        self.difficulty = difficulty
        options = DIFFICULTIES[difficulty]
        self.target_score = int(options["target_score"])
        self.player.reset()
        self.camera.update(ARENA_START, 1.0)
        self.items.reset(None, self.target_score)
        self.score = 0
        self.time_left = settings.GAME_TIME_SECONDS
        self.reef_health = 0.0
        self.ocean.set_reef_health(0.0)
        self.state = "playing"
        self.sharks = [
            Shark(
                1590,
                1170,
                83 * float(options["shark_speed_multiplier"]),
                ARENA_BOUNDS,
                float(options["shark_tracking_distance"]),
            ),
            Shark(
                2380,
                1110,
                94 * float(options["shark_speed_multiplier"]),
                ARENA_BOUNDS,
                float(options["shark_tracking_distance"]),
            ),
            Shark(
                1615,
                1670,
                77 * float(options["shark_speed_multiplier"]),
                ARENA_BOUNDS,
                float(options["shark_tracking_distance"]),
            ),
        ]
        self.jellyfish = [
            Jellyfish(
                self.random.randint(ARENA_BOUNDS[0] + 100, ARENA_BOUNDS[2] - 100),
                self.random.randint(ARENA_BOUNDS[1] + 100, ARENA_BOUNDS[3] - 100),
                speed=self.random.uniform(0.55, 0.85),
                world_bounds=ARENA_BOUNDS,
            )
            for _ in range(int(options["jellyfish_count"]))
        ]

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if self.state == "difficulty_select" and event.key in (
                    pygame.K_1,
                    pygame.K_2,
                    pygame.K_3,
                ):
                    self.reset(("easy", "medium", "hard")[event.key - pygame.K_1])
                elif self.state in ("victory", "game_over") and event.key in (
                    pygame.K_RETURN,
                    pygame.K_KP_ENTER,
                    pygame.K_r,
                ):
                    self.reset()
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.state == "difficulty_select"
            ):
                for difficulty, rect in self.ui.difficulty_button_rects.items():
                    if rect.collidepoint(event.pos):
                        self.reset(difficulty)
                        break
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
            shark.update(dt, target)
        for jellyfish in self.jellyfish:
            jellyfish.update(dt)

        collected = self.items.collect_collisions(self.player.rect)
        self.score = min(
            self.target_score,
            self.score + len(collected) * settings.POLLUTION_SCORE,
        )
        self.reef_health = min(1.0, self.score / self.target_score)
        self.ocean.set_reef_health(self.reef_health)

        for shark in self.sharks:
            if shark.rect.colliderect(self.player.rect):
                self.player.take_damage()
        for jellyfish in self.jellyfish:
            if jellyfish.rect.colliderect(self.player.rect):
                self.player.take_damage()

        if self.score >= self.target_score:
            self.state = "victory"
        elif self.player.health <= 0 or self.time_left <= 0:
            self.state = "game_over"

    def draw(self) -> None:
        self.ocean.draw(self.screen, self.camera)
        self.items.draw(self.screen, self.camera)
        for shark in self.sharks:
            shark.draw(self.screen, self.camera)
        for jellyfish in self.jellyfish:
            jellyfish.draw(self.screen, self.camera)
        self.player.draw(self.screen, self.camera)

        if self.state == "difficulty_select":
            self.ui.draw_difficulty_select(self.screen, pygame.mouse.get_pos())
        elif self.state == "playing":
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
                self.target_score,
                self.player.boost_energy,
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
