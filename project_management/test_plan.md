# Acceptance test plan

## How the results were obtained

Commit tested: `85e7fda` (18 Oct 2026). Date of the run: 19 Oct 2026.

- **Auto**: a throw-away headless script (not in the repository) that
  imports the real modules. It was written and run with the help of an AI
  assistant. `pygame` could not be installed in that environment, so it was
  replaced by a stub that has only a working `Rect`. That covers config
  loading, highscores, ghost and Pac-Man movement and the death/respawn
  logic. **It does not cover drawing, the keyboard, menus or sound.**
- **Manual**: played in the real game.

## Configuration

| # | Test | Expected | Result |
|---|------|----------|--------|
| C1 | Run with no argument or with two | Usage message, exit code 1, no traceback | **Pass** (Auto) |
| C2 | Missing file, a directory, a file that is not `.json` | `ConfigError` with a clear message | **Pass** (Auto) |
| C3 | Invalid JSON, or JSON that is not an object | Error with the line number | **Pass** (Auto) |
| C4 | `{}` (every key missing) | 8 warnings, every default used | **Pass** (Auto) |
| C5 | Wrong type (`"three"`, `true`), negative number, `lives: 0`, empty file name | Warning; default or clamped to the minimum | **Pass** (Auto) |
| C6 | Unknown key | Warning, ignored, valid keys kept | **Pass** (Auto) |
| C7 | Lines starting with `#` | Ignored | **Pass** (Auto) |
| C8 | Size out of 5-20, level that is not an object, fewer than 10 levels, `levels` not a list | Clamped, skipped, padded with 15x15 levels | **Pass** (Auto) |
| C9 | The shipped `config.json` | One warning: the last level is 20x22 **on purpose**, so the reviewer sees an out-of-range value clamped to 20 | **Pass** (Auto) |

## Gameplay

| # | Test | Expected | Result |
|---|------|----------|--------|
| G1 | Ghost targets of the 4 colours for every Pac-Man cell and direction, in 256 maze sizes (5-20 x 5-20, seed 42) | No exception | **Pass** (Auto). Only seed 42 was used |
| G2 | 15 mazes x 40,000 frames with random Pac-Man input and a forced flee every 700 frames, so speeds 1, 2 and 4 change in the middle of corridors | Ghosts never leave the map, never cross a wall, always stay on a corridor axis | **Pass** (Auto): 855 flee events, 138 ghosts eaten |
| G3 | Same run, Pac-Man | Never crosses a wall | **Pass** (Auto) |
| G4 | Same run, state machine | Ghost touches Pac-Man, dying, death, respawn at the start | **Pass** |
| G5 | Eat a super-pacgum in a corner | Ghosts turn blue and slow down, blink in the last 2.25 s, chase again after 6 s | **Pass** |
| G5b | Eat a second super-pacgum while the ghosts are still blue | The flee time restarts and, at the end, every ghost chases again (past bug: ghosts stuck fleeing) | **Pass** |
| G6 | Eat a ghost while it is blue | +`points_per_ghost`, the ghost goes fast to its corner and chases again after 6 s | **Pass** |
| G7 | Eat every pacgum | Next level; score and lives are kept | **Pass** |
| G8 | Clear the 10 levels (use cheat `N` ten times) | Victory screen, then name entry | **Pass** |
| G9 | Let the time run out (`level_max_time: 5`) | Pac-Man dies and loses a life, the timer restarts. In cheat mode nothing happens | **Pass** |
| G10 | Lose every life (`lives: 1`) | Game over screen with the final score | **Pass** |
| G11 | Pause with `Esc`, resume with `P` or `Esc` | The game and the timer stop, and the pause time is not counted | **Pass** |
| G12 | Pause, then `M` | Back to the main menu, no score saved | **Pass** |
| G13 | Levels of different sizes (default `config.json`) | Maze centred, Pac-Man spawns on a free cell, no crash | **Pass** |

## Highscores and screens

| # | Test | Expected | Result |
|---|------|----------|--------|
| H1 | File does not exist | Empty top 10; the file is created on the first save | **Pass** (Auto) |
| H2 | File empty, `hola`, `{}`, `[1, 2]`, `null`, entry without score, deeply nested brackets | No crash; the next save rewrites a valid file | **Pass** (Auto) |
| H3 | Entries with a name of 11 characters, symbols, empty name, negative, `true` or decimal score | Skipped when loading | **Pass** (Auto) |
| H4 | Save 15 scores | Only the best 10 are kept, sorted from best to worst | **Pass** (Auto) |
| H5 | Path that cannot be written (it is a directory) | Warning on stderr, the game goes on | **Pass** (Auto) |
| H6 | Game over -> Space -> type a name -> Enter | Score saved, back to the main menu, it appears in the top 10 | **Pass** |
| H7 | Victory -> Space -> name -> Enter | Same as H6 | **Pass** |
| H8 | Name entry: 11th character, symbols, Enter on an empty name, Backspace | Ignored / ignored / ignored / deletes | **Pass** |
| H9 | Name made only of spaces | Observation from the code: it is accepted, and the entry looks empty in the menu. Allowed by the subject; use `.strip()` if you do not like it | **Pass** |
| H10 | Main menu: Space, `Q` (instructions), `Esc` | Start, instructions, quit | **Pass** |

## Cheat mode

| # | Test | Expected | Result |
|---|------|----------|--------|
| X1 | `C` | `CHEAT` appears at the top left; pressing again turns it off | **Pass** |
| X2 | Touch a ghost with cheat mode on | Nothing happens | **Pass** |
| X3 | `N` with cheat mode on / off | Level cleared / nothing | **Pass** |
| X4 | `F` with cheat mode on | Ghosts stop, `FROZEN` appears; pressing again moves them | **Pass** |
| X5 | Go to the next level | Cheat mode stays on | **Pass** |

## Code quality and packaging

| # | Test | Expected | Result |
|---|------|----------|--------|
| Q1 | `flake8` on `src/` and `pac-man.py` | No errors | **Pass** (Auto, exit code 0) |
| Q2 | `mypy` with the subject's flags, and `--strict` | No errors | **Pass** |
| Q3 | `make install`, `run`, `debug`, `clean`, `lint` | All rules work | **Pass** |
| P1 | Install and launch the packaged game from the public platform | Fully working | **Not done** |

## Bugs found and fixed

See `blockers.md`. The automated run on 19 Oct found no new bug: C9 (a
level above the maximum in the shipped `config.json`) is kept on purpose to
show the clamping. Everything that failed in the past was found by playing
and is in `blockers.md`.
