"""Small cache for the game's pre-generated transparent PNG sprites."""

from pathlib import Path

import pygame


ASSET_ROOT = Path(__file__).with_name("assets")
_SPRITES: dict[tuple[str, str], pygame.Surface] = {}
_SCALED: dict[tuple[int, tuple[int, int]], pygame.Surface] = {}
_ROTATED: dict[tuple[int, int], pygame.Surface] = {}
_PHOTOS: dict[str, pygame.Surface] = {}
_CROPPED_PHOTOS: dict[tuple[str, tuple[int, int]], pygame.Surface] = {}


def load_sprite(category: str, name: str) -> pygame.Surface:
    """Load one bundled sprite once and return its shared surface."""
    key = (category, name)
    if key not in _SPRITES:
        path = ASSET_ROOT / category / f"{name}.png"
        _SPRITES[key] = pygame.image.load(str(path))
    return _SPRITES[key]


def load_photo(filename: str) -> pygame.Surface:
    """Load one bundled wildlife photograph once."""
    if filename not in _PHOTOS:
        path = ASSET_ROOT / "photos" / filename
        _PHOTOS[filename] = pygame.image.load(str(path))
    return _PHOTOS[filename]


def cropped_photo(filename: str, size: tuple[int, int]) -> pygame.Surface:
    """Scale and center-crop a photograph to fill a fixed card frame."""
    width = max(1, round(size[0]))
    height = max(1, round(size[1]))
    key = (filename, (width, height))
    if key not in _CROPPED_PHOTOS:
        photo = load_photo(filename)
        scale = max(width / photo.get_width(), height / photo.get_height())
        scaled_size = (
            round(photo.get_width() * scale),
            round(photo.get_height() * scale),
        )
        scaled = pygame.transform.smoothscale(photo, scaled_size)
        left = (scaled.get_width() - width) // 2
        top = (scaled.get_height() - height) // 2
        _CROPPED_PHOTOS[key] = scaled.subsurface(
            pygame.Rect(left, top, width, height)
        ).copy()
    return _CROPPED_PHOTOS[key]


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
