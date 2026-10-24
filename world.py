"""World boundaries and the stylized depth-based habitat zones."""

from dataclasses import dataclass

import settings


@dataclass(frozen=True)
class HabitatZone:
    key: str
    name: str
    top: int
    bottom: int
    description: str
    water_color: tuple[int, int, int]


ZONES = (
    HabitatZone(
        "shallows",
        "Coastal Shallows",
        0,
        950,
        "Bright water, seagrass, and sunlight",
        (33, 151, 166),
    ),
    HabitatZone(
        "reef",
        "Reef Habitat",
        950,
        1950,
        "Coral formations and active reef life",
        (15, 89, 133),
    ),
    HabitatZone(
        "deep",
        "Deeper Water",
        1950,
        settings.WORLD_HEIGHT,
        "Dim blue water and rocky outcrops",
        (5, 34, 77),
    ),
)


def zone_at(world_y: float) -> HabitatZone:
    """Return the ecological zone for a bounded world y-coordinate."""
    y = max(0.0, min(settings.WORLD_HEIGHT - 1, world_y))
    for zone in ZONES:
        if zone.top <= y < zone.bottom:
            return zone
    return ZONES[-1]


def depth_at(world_y: float) -> int:
    """Return an approximate game depth, not a real-world measurement."""
    y = max(0.0, min(settings.WORLD_HEIGHT, world_y))
    return round(y / settings.WORLD_HEIGHT * settings.GAME_DEPTH_METERS)


def water_color_at(world_y: float) -> tuple[int, int, int]:
    """Blend smoothly between zone colors around each habitat boundary."""
    y = max(0.0, min(settings.WORLD_HEIGHT, world_y))
    blend_width = 260.0
    for index in range(len(ZONES) - 1):
        boundary = ZONES[index].bottom
        if boundary - blend_width / 2 <= y <= boundary + blend_width / 2:
            amount = (y - (boundary - blend_width / 2)) / blend_width
            first = ZONES[index].water_color
            second = ZONES[index + 1].water_color
            return tuple(round(first[channel] + (second[channel] - first[channel]) * amount) for channel in range(3))
    return zone_at(y).water_color
