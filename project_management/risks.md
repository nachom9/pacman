# Risk analysis

Probability and impact: **L**ow, **M**edium, **H**igh.
Status: **Mitigated** (done in the code), **Open** (still to do).

| # | Risk | Prob. | Impact | Mitigation | Status |
|---|------|-------|--------|------------|--------|
| 1 | The assigned A-Maze-ing package fails | M | H | The call is wrapped; it raises `LevelError` and `main()` prints `Error: maze generator failed for level N: ...` and exits | Mitigated |
| 2 | Config file missing, not JSON, or with invalid values (it is changed during the defence) | H | H | `ConfigLoader` clamps every value to a safe default with a warning, ignores unknown keys, skips bad levels and pads to 10 levels; the file errors give a clear message | Mitigated. Tested (`test_plan.md` C1-C9) |
| 3 | Highscore file missing, empty, corrupt, edited by hand or not writable | H | M | Any read error gives an empty top 10, every invalid entry is skipped on load, and a write error only prints a warning | Mitigated. Tested (H1-H5) |
| 4 | Ghosts leave the map or cross walls after a speed change (normal 2, frightened 1, eaten 4) | H | H | Ghosts choose a direction only at cell centres and each step is clamped so it never passes a centre | Mitigated. Tested with a 600,000-frame simulation (G2) |
| 5 | Maze package replaced during the peer review: other mazes, other sizes | M | M | Nothing depends on a particular maze; the closed "42" cells (value 15) are handled for spawn, pacgums and ghost targets; sizes come from the config (5-20) | Mitigated. Targets tested on 256 sizes (G1) |
| 6 | Non-square mazes break row/column code | M | M | Rows use `len(maze)`, columns use `len(maze[0])`; levels of different sizes are in the default `config.json` | Mitigated (found and fixed 15 Oct) |
| 7 | Sprite sheet or font missing, or the game launched from another folder | M | M | Paths are built from the location of `src/paths.py`; asset loading is in a `try` that prints a clear message and exits | Mitigated by code, not run (see note) |
| 8 | The window is taller than the screen: a 20x20 maze needs about 1250 px | M | M | The window is sized from the largest level and the README says so | **Open**: it is documented, not solved. For the defence, use levels that fit the screen |
| 9 | The program crashes during the review because of an unhandled exception | M | H | Config, generator, assets and highscores are covered by `try`/validation | Partly open: the automated runs found no crash, but every screen still has to be played by hand |
| 10 | Packaging and deployment to Steam / Itch.io are not finished | H | H | None in the repository yet | **Open** |
| 11 | `flake8` or `mypy` fail on the final version | L | M | `flake8` and `mypy` pass; type hints and docstrings everywhere | Mitigated. Re-run `make lint` before submitting |
| 12 | A team member cannot explain code written by the other (recode exercise) | M | H | Each one reviews and explains the other's modules before the defence. The history shows both worked on `level.py`, `__main__.py` and `ghosts.py` | **Open** |
| 13 | Cheat mode does not let the reviewer reach every feature | L | M | `C` invincibility (also against the time limit), `N` skips the level, `F` freezes ghosts; lives and time are changed in the config | Mitigated. Manual check pending (X1-X5) |

Note on 7: asset loading was not run in the automated checks because `pygame`
could not be installed in the environment used for them.
