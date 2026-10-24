"""Attribution metadata for real wildlife photos used on discovery cards."""

import json
from pathlib import Path


_MANIFEST_PATH = Path(__file__).with_name("assets") / "photos" / "manifest.json"
with _MANIFEST_PATH.open(encoding="utf-8") as manifest_file:
    WILDLIFE_PHOTOS: dict[str, dict[str, str]] = json.load(manifest_file)
