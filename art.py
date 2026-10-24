"""Small cache for the game's pre-generated transparent PNG sprites."""

from pathlib import Path

import pygame


ASSET_ROOT = Path(__file__).with_name("assets")
_SPRITES: dict[tuple[str, str], pygame.Surface] = {}
_SCALED: dict[tuple[int, tuple[int, int]], pygame.Surface] = {}
_ROTATED: dict[tuple[int, int], pygame.Surface] = {}


def load_sprite(category: str, name: str) -> pygame.Surface:
    """Load one bundled sprite once and return its shared surface."""
    key = (category, name)
    if key not in _SPRITES:
        path = ASSET_ROOT / category / f"{name}.png"
        _SPRITES[key] = pygame.image.load(str(path))
    return _SPRITES[key]


def scaled_sprite(
    sprite: pygame.Surface,
    size: tuple[int, int],
) -> pygame.Surface:
    """Nearest-neighbor scale and cache pixel-inspired artwork."""
    width = max(1, round(size[0]))
    height = max(1, round(size[1]))
    key = (id(sprite), (width, height))
    if key not in _SCALED:
        _SCALED[key] = pygame.transform.scale(sprite, (width, height))
    return _SCALED[key]


def rotated_sprite(sprite: pygame.Surface, degrees: float) -> pygame.Surface:
    """Cache a small set of gently swayed sprite rotations."""
    angle = round(degrees / 5) * 5
    key = (id(sprite), angle)
    if key not in _ROTATED:
        _ROTATED[key] = pygame.transform.rotate(sprite, angle)
    return _ROTATED[key]
