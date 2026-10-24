# Tidekeeper

Tidekeeper is a 2D side-view underwater exploration and restoration game built with Python 3 and Pygame. Explore stylized Gulf Reef and Mediterranean Sea regions, inspect illustrated wildlife and environmental objects, and launch a separate cleanup game window. The game uses original, locally generated transparent PNG artwork; it does not download images or require a network connection to play.

The world is approximately 4,000 x 3,000 game pixels. It is a stylized prototype, not a scientifically accurate map or water-depth simulation. Wildlife descriptions link to agency or museum references; the illustrations and locations are stylized representations, not field-identification artwork or mapped sightings.

## Requirements

- Python 3.10 or newer
- Pygame 2.5 or newer
- Pillow 10 or newer (only needed to regenerate the artwork)

## Install and run

Open a terminal in the project folder. A virtual environment keeps the game dependency separate from other Python projects.

### macOS

After setting up the dependencies below, you can launch the game by double-clicking `launch_tidekeeper.command` in Finder. If macOS blocks it the first time, right-click the file, choose **Open**, and confirm.

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
- Hold **Shift** — use the limited speed boost shown in the HUD; release to recharge after a short delay
- **Click a region** — choose Gulf of Mexico, Mediterranean Sea, Arctic Ocean, Great Lakes, or Amazon River
- **Click Explore or Play** — choose the activity for the selected region
- **E** or **Enter** — start Explore from the activity menu
- **P** — launch the selected region's separate Play window
- **Escape** — close a card, return from Explore to the activity menu, or close the Play window
- **Backspace** — return from the activity menu to region selection
- **Click an organism, habitat, or pollutant** — open its fact and environmental-impact card
- **F** — when near visible wildlife, fish, litter, coral, or plants, open its information card; close an open card
- **Click the source link** — open the cited agency or museum reference
- **R** — restart after winning or losing
- **Mouse** — use the menu buttons

### Explore World

The first menu selects one of five regions; the second offers Explore or Play for the selected region. Explore is a free-roaming world with no timer, damage, or mission collection. Gulf Reef contains Gulf-associated fish, wildlife, reef habitats, and seagrass. Mediterranean Sea features clear blue water with a rose tint, pale rocky formations, Posidonia oceanica meadows, a coastal rock arch, and a stylized amphora. The Arctic Ocean uses icy light, kelp, sea ice, cod, narwhal, and ringed seal; Great Lakes features blue-green freshwater, wild rice, native fish, mussels, and a shipwreck; Amazon River brings warm tea-colored water, flooded forest, water lilies, and Amazonian freshwater wildlife. Each new area includes limited, region-specific debris rather than a general trash field. Click visible wildlife, fish, habitats, plants, landmarks, or litter to read region-specific facts, environmental impacts, and source links. **Inspect: press F** near an object to open its card. The HUD shows boost charge, current habitat, and approximate **game depth**.

### Cleanup game window

The second menu's **Play** button launches the selected region in a separate cleanup-game window. All five regions share the cleanup controls and difficulty options, but use region-specific water, wildlife, diver, and debris artwork. Hazards and pursuing wildlife vary by region. Choose Easy, Medium, or Hard before starting. The expanded map begins with enough randomly placed pieces of waste to complete the selected objective, with no replacement spawns. Easy has 6 hazards and 10 pieces to collect, Medium has 9 and 15, and Hard has 12 and 20. Collect all required pieces before the 120-second timer runs out. The diver has three hearts and a short invulnerability window after taking a hit. **R** or **Enter** restarts after a result; **Escape** closes the game window. The exploration window stays separate.

## World and camera

The camera follows the diver smoothly and stops at the edges of the 4,000 x 3,000 world. The diver, pollution, jellyfish, plants, rocks, ambient fish, and discoverable organisms use world coordinates. Renderers convert those positions through `camera.py`; HUD elements stay at fixed screen positions.

`world.py` selects the current stylized habitat from the diver's vertical position for the active region. Each region has its own water palette, tint, zones, original backdrop, terrain, plant life, wildlife, and pollution artwork. The regions use composed clusters of terrain, plants, landmarks, and schooling fish while retaining open swim paths. A distant image layer shifts more slowly than the world while foreground plants drift slightly faster; clickable wildlife and pollution stay aligned with their world coordinates. Displayed depth is an approximate game value, not a claim about real-world depth. Decorative placements use a fixed seed and only nearby objects are drawn.

## Project files

- `main.py` — game loop, state/mode switching, camera integration, collisions, scoring, and end conditions.
- `play_window.py` — standalone compact cleanup mission launched from the exploration window.
- `settings.py` — shared window, world, movement, and gameplay values.
- `camera.py` — smooth following, world-to-screen conversion, and viewport checks.
- `art.py` — cached loading, scaling, and rotation of bundled PNG sprites.
- `world.py` — world size, habitat zones, color transitions, and approximate game-depth calculation.
- `player.py` — diver movement, world boundaries, health, boost, sprite animation, and bubble trail.
- `ocean.py` — depth-colored water, lighting, parallax backdrop, textured seabed, composed reef groups, and animated fish schools.
- `enemies.py` — Explore and Play predator movement, regional artwork, and collision rectangles.
- `items.py` — pollution placement, animation, collection, and pickup effects.
- `wildlife.py` — clickable points of interest, illustrated organisms and pollutants, and session discovery tracking.
- `ecology_data.py` — Gulf-themed profile text, habitat labels, world positions, and source links.
- `mediterranean_data.py` — Mediterranean wildlife and habitat cards, pollution profiles, and reference links.
- `arctic_data.py`, `great_lakes_data.py`, and `amazon_data.py` — regional discovery profiles, pollution types, and research references.
- `region_data.py` — shared region labels, tints, wildlife, habitat, hazard, and pollution lookups.
- `ui.py` — menu, fixed HUD, habitat notices, discovery card, and results screens.
- `assets/` — generated diver, regional wildlife, fish, reef, plant, terrain, landmark, background, and bubble PNGs.
- `tools/generate_assets.py` — offline Pillow script that creates the PNG artwork once; the game does not run it.
- `requirements.txt` — Pygame and Pillow dependencies.

### Artwork and regeneration

The custom PNG library includes separate diver, fish, wildlife, habitat, debris, landmark, seafloor, backdrop, and bubble artwork for each region, along with Gulf coral forms and Mediterranean Posidonia. The Arctic, Great Lakes, and Amazon sets can be regenerated without overwriting existing regional art:

To regenerate the artwork after editing the generator, install the project requirements and run:

```bash
python tools/generate_assets.py --new-regions
```

Run `python tools/generate_assets.py` to regenerate the full original artwork library. The game loads saved PNGs at startup and caches commonly used scaled surfaces. Pillow is not imported by the runtime game modules.

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
