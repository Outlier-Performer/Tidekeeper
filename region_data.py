"""Shared region names, tint, and ecology profile lookups."""

from amazon_data import (
    ENVIRONMENT_PROFILES as AMAZON_ENVIRONMENT_PROFILES,
    HAZARD_NAME as AMAZON_HAZARD_NAME,
    HAZARD_PROFILE_ID as AMAZON_HAZARD_PROFILE_ID,
    POLLUTION_PROFILES as AMAZON_POLLUTION_PROFILES,
    PREDATOR_NAME as AMAZON_PREDATOR_NAME,
    WILDLIFE_PROFILES as AMAZON_WILDLIFE_PROFILES,
)
from arctic_data import (
    ENVIRONMENT_PROFILES as ARCTIC_ENVIRONMENT_PROFILES,
    HAZARD_NAME as ARCTIC_HAZARD_NAME,
    HAZARD_PROFILE_ID as ARCTIC_HAZARD_PROFILE_ID,
    POLLUTION_PROFILES as ARCTIC_POLLUTION_PROFILES,
    PREDATOR_NAME as ARCTIC_PREDATOR_NAME,
    WILDLIFE_PROFILES as ARCTIC_WILDLIFE_PROFILES,
)
from ecology_data import ENVIRONMENT_PROFILES as GULF_ENVIRONMENT_PROFILES
from ecology_data import POLLUTION_PROFILES as GULF_POLLUTION_PROFILES
from ecology_data import WILDLIFE_PROFILES as GULF_WILDLIFE_PROFILES
from great_lakes_data import (
    ENVIRONMENT_PROFILES as GREAT_LAKES_ENVIRONMENT_PROFILES,
    HAZARD_NAME as GREAT_LAKES_HAZARD_NAME,
    HAZARD_PROFILE_ID as GREAT_LAKES_HAZARD_PROFILE_ID,
    POLLUTION_PROFILES as GREAT_LAKES_POLLUTION_PROFILES,
    PREDATOR_NAME as GREAT_LAKES_PREDATOR_NAME,
    WILDLIFE_PROFILES as GREAT_LAKES_WILDLIFE_PROFILES,
)
from mediterranean_data import (
    ENVIRONMENT_PROFILES as MEDITERRANEAN_ENVIRONMENT_PROFILES,
    POLLUTION_PROFILES as MEDITERRANEAN_POLLUTION_PROFILES,
    WILDLIFE_PROFILES as MEDITERRANEAN_WILDLIFE_PROFILES,
)

REGION_IDS = ("gulf", "mediterranean", "arctic", "great_lakes", "amazon")
REGION_LABELS = {
    "gulf": "GULF OF MEXICO",
    "mediterranean": "MEDITERRANEAN SEA",
    "arctic": "ARCTIC OCEAN",
    "great_lakes": "GREAT LAKES",
    "amazon": "AMAZON RIVER",
}
REGION_NAMES = {
    "gulf": "Gulf of Mexico",
    "mediterranean": "Mediterranean Sea",
    "arctic": "Arctic Ocean",
    "great_lakes": "Great Lakes",
    "amazon": "Amazon River",
}
REGION_TINTS: dict[str, tuple[int, int, int, int] | None] = {
    "gulf": None,
    "mediterranean": (235, 70, 88, 88),
    "arctic": (218, 238, 255, 92),
    "great_lakes": (37, 177, 154, 54),
    "amazon": (255, 126, 121, 78),
}
REGION_WILDLIFE_PROFILES = {
    "gulf": GULF_WILDLIFE_PROFILES,
    "mediterranean": MEDITERRANEAN_WILDLIFE_PROFILES,
    "arctic": ARCTIC_WILDLIFE_PROFILES,
    "great_lakes": GREAT_LAKES_WILDLIFE_PROFILES,
    "amazon": AMAZON_WILDLIFE_PROFILES,
}
REGION_ENVIRONMENT_PROFILES = {
    "gulf": GULF_ENVIRONMENT_PROFILES,
    "mediterranean": MEDITERRANEAN_ENVIRONMENT_PROFILES,
    "arctic": ARCTIC_ENVIRONMENT_PROFILES,
    "great_lakes": GREAT_LAKES_ENVIRONMENT_PROFILES,
    "amazon": AMAZON_ENVIRONMENT_PROFILES,
}
REGION_POLLUTION_PROFILES = {
    "gulf": GULF_POLLUTION_PROFILES,
    "mediterranean": MEDITERRANEAN_POLLUTION_PROFILES,
    "arctic": ARCTIC_POLLUTION_PROFILES,
    "great_lakes": GREAT_LAKES_POLLUTION_PROFILES,
    "amazon": AMAZON_POLLUTION_PROFILES,
}
REGION_HAZARD_PROFILE_IDS = {
    "gulf": "moon_jellyfish",
    "mediterranean": "moon_jellyfish",
    "arctic": ARCTIC_HAZARD_PROFILE_ID,
    "great_lakes": GREAT_LAKES_HAZARD_PROFILE_ID,
    "amazon": AMAZON_HAZARD_PROFILE_ID,
}
REGION_HAZARD_NAMES = {
    "gulf": "jellyfish",
    "mediterranean": "jellyfish",
    "arctic": ARCTIC_HAZARD_NAME,
    "great_lakes": GREAT_LAKES_HAZARD_NAME,
    "amazon": AMAZON_HAZARD_NAME,
}
REGION_PREDATOR_NAMES = {
    "gulf": "Sharks",
    "mediterranean": "Barracuda",
    "arctic": ARCTIC_PREDATOR_NAME,
    "great_lakes": GREAT_LAKES_PREDATOR_NAME,
    "amazon": AMAZON_PREDATOR_NAME,
}


def normalize_region_id(region_id: str) -> str:
    """Return a known region ID, defaulting to the original Gulf region."""
    return region_id if region_id in REGION_IDS else "gulf"
