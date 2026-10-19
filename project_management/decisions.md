# Technical decisions and team organisation

## Team organisation

Two members. Roles come from the git history (34 commits each, 68 in
total); `git blame` and `git log -- <file>` show the detail.

| Member | Main areas |
|--------|------------|
| imelero- (git: Nacho) | Maze drawing, sprites, Pac-Man movement and collisions, death animation, the four ghosts (BFS, targets, flee and eaten modes), game over and name entry screens, saving highscores, main loop back to the menu, first version of the cheat mode |
| dvallada (git: DiegoVa6, Diego Valladares) | HUD, main / pause / instructions menus, level timer with pause, `uv` + Makefile + `flake8` + `mypy`, config loader, `Level` class, levels of different sizes, `GameStats`, victory screen, time limit, highscore validation, entry point and asset paths, type hints and docstrings, README |

Several files were edited by both (`level.py`, `__main__.py`, `ghosts.py`,
`pacman.py`, `scores.py`, `name_entry.py`), so everybody has to be able to
explain them.

- **How we worked:** short feature branches (`ghosts-flee`, `screens`,
  `nacho`) merged into `main`; the team board is GitHub Projects / Issues.
- **How decisions were taken:** we met in person to discuss and make decisions
  together, and stayed in touch via chat every day to share our progress,
  coordinate tasks, make quick decisions as needed, and ensure we stayed
  aligned throughout the project.
- **How problems were handled:** see `blockers.md`.

## Technical decisions

### Graphics library: pygame
Windows, surfaces, blitting, events and fonts. Every function we use has an
MLX-like equivalent, as the subject asks.

### Maze: use the generator's wall bits directly
Each cell is a number with 4 bits (1 up, 2 right, 4 down, 8 left). The
same data draws the walls (`DrawnMaze`), gives the wall rects for Pac-Man's
collisions, and lets the ghosts' BFS know which neighbours are reachable.
`perfect=False` gives loops, so the ghosts cannot trap the player. The
generator draws a "42" of closed cells (value 15), so pacgums are not
placed there and Pac-Man spawns on the free cell closest to the centre.

### Ghost movement: decide only at cell centres
A ghost chooses its direction with BFS only when it is exactly at the
centre of a cell. Between centres it goes straight and each step is cut so
it never passes the next centre. It works with any speed (1 frightened,
2 normal, 4 eaten) even though 54 px is not a multiple of 4. The last step
of a cell can be shorter, so the average speed at 4 is about 3.5 % lower,
which cannot be seen. The first version patched the alignment for each
speed and failed (see `blockers.md`).

### Ghost behaviours
Red goes to Pac-Man's cell, pink to 4 cells ahead, orange to 4 cells behind
and blue to the red ghost mirrored over the cell 2 cells ahead of Pac-Man.
After a super-pacgum the ghosts go slowly to their corner for 6 s, blinking
in the last 2.25 s; a ghost that is eaten goes back fast and chases again
after 6 s.

### Config: JSON with `#` comments and a validating loader
Comment lines are blanked before parsing, so line numbers in errors stay
right. Each key is checked on its own; the loader warns and keeps a default
instead of failing, as the subject asks. Only a file that cannot be used at
all (missing, not JSON, not an object) stops the game, with a clear message.

### Highscores: one JSON file and stateless functions
- JSON can be read and edited by hand, which helps to test the validation
  in the peer review; it needs no dependency.
- `load_scores` and `save_score` are plain functions in `scores.py`: there
  is no state to keep.
- Validation is done on **loading**, so a file edited by hand cannot break
  the menu; the name entry already limits what can be typed.
- The menu reads the file each time it opens, so a new score shows at once.
- The file name comes from `highscore_filename` in the config.

### Shared game state: `GameStats`
Score, lives and the cheat flags live in one object created for each game
and passed to every level. This is how score and lives are kept from one
level to the next, as the subject requires, and a new game always starts
from zero.

### Game loop: `while` around a `for ... else`
`main()` starts everything once. Then it loops: main menu, one `Level` per
config entry, and back to the menu. The `else` of the `for` runs only when
no level did `break`, so the victory screen appears only after clearing
every level. `Level.run()` returns a string (`"cleared"`, `"menu"`,
`"score saved"`, `"quit"`) and `main()` decides what comes next.

### Screens as classes with `draw()` and `run()`
Menus and end screens (`MainMenu`, `PauseMenu`, `DeathEndGame`,
`VictoryScreen`, `NameEntry`) each own their loop and return a string
that says what the player chose. `Level` and `main()` only coordinate them.

### Time limit: lose a life
When the level time ends, Pac-Man dies as if a ghost had caught him and the
timer starts again. The pacgums already eaten stay eaten. The subject
leaves this choice open. The time spent in pause is not counted.

### Leaving from the pause menu
`M` in the pause menu goes back to the main menu and the game is lost
without saving a score, because the game did not end by winning or losing.
It is written in the README.

### Cheat mode
`C` turns it on and off. While it is on Pac-Man cannot die (neither from
ghosts nor from the time limit) and `CHEAT` is shown. `N` clears the level
and `F` freezes the ghosts. It stays on between levels. Lives and the time
limit are not cheats because the reviewer changes them in the config.

### Window size
Each cell is 54 px and the window grows with the largest level, with a
minimum of 640x900 so the menus fit. The reason is simplicity; the
drawback is that a 20x20 maze needs about 1250 px of screen height
(`risks.md`, risk 8).

### Tooling
`uv` for the virtual environment and dependencies (the maze generator is
installed from the local `.whl`), `flake8`, `mypy --strict`, type hints and
docstrings everywhere. Asset paths are built from the location of
`src/paths.py`, so the game runs from any folder.
