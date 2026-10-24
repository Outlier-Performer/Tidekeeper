# Tidekeeper

Tidekeeper is a 2D side-view underwater exploration and restoration game built with Python 3 and Pygame. Explore a large stylized Gulf of Mexico-inspired world, inspect illustrated wildlife and environmental objects, and launch a separate cleanup game window. The game uses original, locally generated transparent PNG artwork; it does not download images or require a network connection to play.

The world is approximately 4,000 x 3,000 game pixels. It is a stylized prototype, not a scientifically accurate map or water-depth simulation. Wildlife descriptions link to agency or museum references; the illustrations and locations are stylized representations, not field-identification artwork or mapped sightings.

## Requirements

- Python 3.10 or newer
- Pygame 2.5 or newer
- Pillow 10 or newer (only needed to regenerate the artwork)

## Install and run

Open a terminal in the project folder. A virtual environment keeps the game dependency separate from other Python projects.

### macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

### Windows

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

If PowerShell blocks activation, use Command Prompt and run `.venv\Scripts\activate.bat`. Pygame can also be installed directly with `python -m pip install pygame`.

## Controls

- **WASD** or **arrow keys** — swim in four directions
- **Space** — swim faster while held
- **Enter** or **E** — start exploring from the menu
- **Click Explore World** — open the Gulf exploration world
- **Click Open Play Window** or press **P** — launch the separate cleanup game window
- **Click an organism, habitat, or pollutant** — open its fact and environmental-impact card
- **F** — inspect the nearest point of interest; close its card
- **Click the source link** — open the cited agency or museum reference
- **Escape** — close a card, then return to the exploration menu
- **R** — restart after winning or losing
- **Mouse** — use the menu buttons

### Explore World

The main window is a free-roaming world with no timer, damage, or mission collection. It contains original PNG artwork for Gulf-associated fish, wildlife, reef habitats, and seagrass, alongside illustrated plastic litter, cans, oil slicks, and lost fishing gear. Click visible points of interest to read a short fact, environmental impact, and source link. Organisms move independently around stable patrol paths. The HUD shows the current stylized habitat and approximate **game depth**.

### Cleanup game window

The menu's **Open Play Window** button (or **P** while exploring) launches a separate desktop window for the compact cleanup mission. It has its own diver, timer, health, pollution, and chasing Gulf-shark illustrations. Collect 10 pieces of waste before the 120-second timer runs out. The diver has three hearts and a short invulnerability window after taking a hit. **R** or **Enter** restarts after a result; **Escape** closes that game window. The exploration window stays separate.

## World and camera

The camera follows the diver smoothly and stops at the edges of the 4,000 x 3,000 world. The diver, pollution, jellyfish, plants, rocks, ambient fish, and discoverable organisms use world coordinates. Renderers convert those positions through `camera.py`; HUD elements stay at fixed screen positions.

`world.py` selects the current stylized habitat from the diver's vertical position. Coastal Shallows, Reef Habitat, and Deeper Water have smoothly blended background colors. The reef uses deliberate clusters of rocks, coral, plants, and small schooling fish, with an open swim corridor through the main formation. A distant image layer shifts more slowly than the world while the foreground plants drift slightly faster; clickable wildlife and pollution stay aligned with their world coordinates. Displayed depth is an approximate game value, not a claim about real-world depth. Decorative placements use a fixed seed and only nearby objects are drawn.

## Project files

- `main.py` — game loop, state/mode switching, camera integration, collisions, scoring, and end conditions.
- `play_window.py` — standalone compact cleanup mission launched from the exploration window.
- `settings.py` — shared window, world, movement, and gameplay values.
- `camera.py` — smooth following, world-to-screen conversion, and viewport checks.
- `art.py` — cached loading, scaling, and rotation of bundled PNG sprites.
- `world.py` — world size, habitat zones, color transitions, and approximate game-depth calculation.
- `player.py` — diver movement, world boundaries, health, boost, sprite animation, and bubble trail.
- `ocean.py` — depth-colored water, lighting, parallax backdrop, textured seabed, composed reef groups, and animated fish schools.
- `enemies.py` — Explore-mode jellyfish and Play-window shark movement, artwork, and collision rectangles.
- `items.py` — pollution placement, animation, collection, and pickup effects.
- `wildlife.py` — clickable points of interest, illustrated organisms and pollutants, and session discovery tracking.
- `ecology_data.py` — Gulf-themed profile text, habitat labels, world positions, and NOAA source links.
- `ui.py` — menu, fixed HUD, habitat notices, discovery card, and results screens.
- `assets/` — generated diver, wildlife, fish, reef, plant, terrain, background, and bubble PNGs.
- `tools/generate_assets.py` — offline Pillow script that creates the PNG artwork once; the game does not run it.
- `requirements.txt` — Pygame and Pillow dependencies.

### Artwork and regeneration

The custom PNG library includes a 128 x 88 diver, three distinct Gulf-associated fish illustrations (red snapper, blue tang, and queen angelfish), four clickable wildlife illustrations, three coral forms, seagrass and sargassum, two reef rocks, a 256 x 96 sandy-floor tile, a 1600 x 700 transparent parallax backdrop, and a reusable bubble sprite. Sprites use transparent backgrounds where appropriate and nearest-neighbor scaling to retain their pixel-inspired edges.

To regenerate the artwork after editing the generator, install the project requirements and run:

```bash
python tools/generate_assets.py
```

The game loads the saved PNGs at startup and caches commonly used scaled surfaces. Pillow is not imported by the runtime game modules.

## Module interfaces and teamwork

`main.py` owns the exploration session. The player and all world entities retain world-space coordinates; their `draw(screen, camera)` methods render them in view. Moving systems use `update(dt, ...)`. Clicking a profile in `wildlife.py` or a pollution collectible opens a card rendered by `ui.py`; its source link opens the cited agency or museum page. `play_window.py` runs as a separate process so it creates a distinct Pygame desktop window while reusing the player, camera, ocean, item, shark, and UI modules.

Avoid changing shared interfaces without coordinating, especially `Camera.world_to_screen`, `Camera.update`, entity `draw(screen, camera)`, player `rect` and `x/y`, `PollutionField.collect_collisions`, and the `ecology_data.py` profile fields (`kind`, `illustration`, `position`, `fact`, `impact`, and `source`).

Suggested split:

1. Developer 1: `main.py`, `player.py`, `camera.py`, and `play_window.py` (input, movement, and game flow).
2. Developer 2: `ocean.py`, `enemies.py`, `world.py`, and the illustration methods in `wildlife.py`.
3. Work together on `items.py`, `ecology_data.py`, and `ui.py`, since they connect collection, source-backed information, and display.
4. Use separate GitHub Desktop branches, coordinate interface changes before merging, and test the merged game with `python main.py`.

## Research note

The illustrations are original pixel-inspired artwork, not photographs. They are stylized representations, not field-identification art; ambient fish are illustrative and are not individual wildlife sightings. Information cards link to NOAA, Florida Fish and Wildlife Conservation Commission, or Florida Museum references. The world and object locations are illustrative and do not map actual Gulf spill sites.
