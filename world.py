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

MEDITERRANEAN_ZONES = (
    HabitatZone(
        "coastal_shelf",
        "Coastal Shelf",
        0,
        520,
        "Clear shallows and pale coastal stone",
        (53, 169, 198),
    ),
    HabitatZone(
        "posidonia",
        "Posidonia Meadow",
        520,
        1350,
        "Seagrass blades shelter a lively meadow",
        (32, 120, 157),
    ),
    HabitatZone(
        "rocky_slope",
        "Rocky Slope",
        1350,
        settings.WORLD_HEIGHT,
        "Cool blue water around rugged rock",
        (13, 57, 92),
    ),
)

ARCTIC_ZONES = (
    HabitatZone("ice_edge", "Ice Edge", 0, 700, "Pale light beneath shifting sea ice", (187, 225, 243)),
    HabitatZone("cold_shelf", "Cold Shelf", 700, 1700, "Arctic cod, seals, and cold-water life", (105, 165, 194)),
    HabitatZone("deep_arctic", "Deep Arctic", 1700, settings.WORLD_HEIGHT, "Dim blue water and rocky northern seafloor", (41, 88, 125)),
)

GREAT_LAKES_ZONES = (
    HabitatZone("nearshore", "Nearshore Shoals", 0, 650, "Shallow blue-green water and aquatic plants", (48, 157, 160)),
    HabitatZone("open_lake", "Open Lake", 650, 1900, "Cool freshwater with schools of native fish", (31, 113, 139)),
    HabitatZone("lakebed", "Deep Lakebed", 1900, settings.WORLD_HEIGHT, "Quiet water above the rocky lake floor", (20, 70, 101)),
)

AMAZON_ZONES = (
    HabitatZone("floodplain", "Floodplain Margin", 0, 650, "Sunlit water and floating leaves", (139, 130, 106)),
    HabitatZone("flooded_forest", "Flooded Forest", 650, 1800, "Submerged roots shelter river life", (116, 98, 91)),
    HabitatZone("river_channel", "River Channel", 1800, settings.WORLD_HEIGHT, "Deeper, tea-colored freshwater", (79, 68, 78)),
)


def zones_for(region_id: str = "gulf") -> tuple[HabitatZone, ...]:
    return {
        "mediterranean": MEDITERRANEAN_ZONES,
        "arctic": ARCTIC_ZONES,
        "great_lakes": GREAT_LAKES_ZONES,
        "amazon": AMAZON_ZONES,
    }.get(region_id, ZONES)


def zone_at(world_y: float, region_id: str = "gulf") -> HabitatZone:
    """Return the ecological zone for a bounded world y-coordinate."""
    y = max(0.0, min(settings.WORLD_HEIGHT - 1, world_y))
    zones = zones_for(region_id)
    for zone in zones:
        if zone.top <= y < zone.bottom:
            return zone
    return zones[-1]


def depth_at(world_y: float) -> int:
    """Return an approximate game depth, not a real-world measurement."""
    y = max(0.0, min(settings.WORLD_HEIGHT, world_y))
    return round(y / settings.WORLD_HEIGHT * settings.GAME_DEPTH_METERS)


def water_color_at(
    world_y: float,
    region_id: str = "gulf",
) -> tuple[int, int, int]:
    """Blend smoothly between zone colors around each habitat boundary."""
    y = max(0.0, min(settings.WORLD_HEIGHT, world_y))
    zones = zones_for(region_id)
    blend_width = 260.0
    for index in range(len(zones) - 1):
        boundary = zones[index].bottom
        if boundary - blend_width / 2 <= y <= boundary + blend_width / 2:
            amount = (y - (boundary - blend_width / 2)) / blend_width
            first = zones[index].water_color
            second = zones[index + 1].water_color
            return tuple(round(first[channel] + (second[channel] - first[channel]) * amount) for channel in range(3))
    return zone_at(y, region_id).water_color
