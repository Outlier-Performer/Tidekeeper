# Tidekeeper

Tidekeeper is a small 2D underwater exploration and ocean-restoration game made with Python 3 and Pygame. Swim around the reef, collect floating plastic and cans, avoid jellyfish, and watch the ocean brighten as you restore it.

This is a self-contained MVP: all graphics are drawn with Pygame, so no image, music, or other asset downloads are needed.

## Requirements

- Python 3.10 or newer
- Pygame 2.5 or newer

## Install and run

Open a terminal in the project folder. Using a virtual environment is recommended so the game dependency stays separate from other Python projects.

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

If PowerShell blocks virtual-environment activation, use Command Prompt and run `.venv\Scripts\activate.bat` instead. You can also install Pygame directly with `python -m pip install pygame`.

## Controls

- **WASD** or **arrow keys** — swim
- **Space** — swim faster while held
- **Enter** — start from the menu or play again
- **R** — restart after winning or losing
- **Escape** — return to the menu during a game
- **Mouse** — click the menu's Start button

Collect 10 pieces of pollution before the 120-second timer runs out. Each piece adds points and improves reef health. Avoid jellyfish: each hit costs a heart, with a brief invulnerability window to prevent repeated damage from one collision. The player starts with three hearts.

## Project files

- `main.py` — initializes Pygame, runs the game loop, and changes between menu, play, victory, and game-over states.
- `settings.py` — shared window, gameplay, and color constants.
- `player.py` — player movement, boundaries, health, boost, and swimming animation.
- `ocean.py` — animated water, light, bubbles, seaweed, coral, and reef-health visuals.
- `enemies.py` — jellyfish movement, drawing, and collision rectangles.
- `items.py` — pollution spawning and animation, collection, score values, and collection effects.
- `ui.py` — menu, start button, HUD, timer, and end screens.
- `requirements.txt` — the Pygame dependency.

## How the modules work together

`main.py` owns the current game state and the main update/draw loop. Each frame it passes elapsed seconds (`dt`) to moving objects, checks collisions, and updates the reef-health value. The player, jellyfish, pollution field, and ocean use a small shared convention: `update(dt)` changes their state and `draw(screen)` renders them. `items.py` reports collected pollution to `main.py`; the game loop updates the score and passes the resulting reef health to `ocean.py` and `ui.py`. Shared values live in `settings.py`.

To keep the modules easy to work on together, coordinate before changing public method names, constructor arguments, or values shared between `main.py` and another module (especially `update(dt)`, `draw(screen)`, player health, and pollution collection results).

## A simple way to work as a pair

1. Developer 1 can focus on `main.py` and `player.py`, including movement and game flow.
2. Developer 2 can focus on `ocean.py` and `enemies.py`, including atmosphere and creature behavior.
3. Both developers can make separate branches in GitHub Desktop, agree on shared interfaces before changing them, and merge/test one branch at a time.
4. `items.py`, `ui.py`, and `settings.py` are shared integration points. Keep changes small and let the other developer know when changing their constants or method signatures.
5. After merging, run `python main.py` and test the full round: collect pollution, take damage, win, lose, and restart.

## Ideas for future features

- Add a rescued fish that follows the player and returns to a safe reef zone.
- Give each pollution type a different cleanup action or point value.
- Add a short dash cooldown or air meter to make boost timing a choice.
- Introduce a reef-restoration objective, such as planting coral in marked areas.
- Create a second area with different currents, creatures, and cleanup goals.
