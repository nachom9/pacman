"""Absolute paths to the game assets.

The paths are built from the location of this file, not from the folder
the game is launched from, so the game finds its assets wherever it is run.
"""

from pathlib import Path

# Project root: the folder that contains src/ (this file is src/paths.py).
PROJECT_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_DIR / "assets"
FONT_PATH = str(ASSETS_DIR / "fonts" / "PressStart2P-Regular.ttf")
SPRITES_PATH = str(ASSETS_DIR / "sprites.png")
