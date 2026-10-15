#!/usr/bin/env python3

from src.hud import HUD
from src.level import BOTTOM_SPACE, TOP_SPACE, Level, LevelError
from src.level import maze_pixel_size
from src.main_menu import MainMenu
from src.pause_menu import PauseMenu
from src.death_end_game import DeathEndGame
from src.game_stats import GameStats
from src.name_entry import NameEntry
from src.parse_entry import ConfigLoader, ConfigError, LevelConfig
from src.victory_screen import VictoryScreen
import sys
import pygame


def check_arguments() -> str:
    """Return the config path given on the command line, or exit."""
    if len(sys.argv) != 2:
        print(
            "Error: expected exactly one argument, the config file.\n"
            "Usage: python3 pac-man.py config.json",
            file=sys.stderr,
        )
        sys.exit(1)
    return sys.argv[1]


def main():
    file_path = check_arguments()
    config = ConfigLoader(file_path)
    try:
        config.load_config()
    except ConfigError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    max_width = max(level.width for level in config.levels)
    max_height = max(level.height for level in config.levels)
    maze_w, maze_h = maze_pixel_size(max_width, max_height)

    pygame.init()
    screen = pygame.display.set_mode(
        (maze_w, maze_h + TOP_SPACE + BOTTOM_SPACE)
    )
    clock = pygame.time.Clock()
    pygame.display.set_caption("Pacman")

    menu = MainMenu(screen.get_width(), screen.get_height())

    try:
        spritesheet = pygame.image.load("assets/sprites.png").convert_alpha()
    except (FileNotFoundError, pygame.error) as e:
        print(
            f"Error: cannot load 'assets/sprites.png': {e}\n"
            "Make sure the file exists and run the game from the project root.",
            file=sys.stderr,
        )
        pygame.quit()
        sys.exit(1)

    width, height = screen.get_width(), screen.get_height()
    hud = HUD(width, height, spritesheet)
    pause_menu = PauseMenu(width, height)
    death_end_game = DeathEndGame(width, height)
    name_entry = NameEntry(width, height)
    victory_screen = VictoryScreen(width, height)


    playing = True
    while playing:
        if menu.run(screen, clock) == "quit":
            pygame.quit()
            return
        first = True
        stats = GameStats(config.lives)
        for index, level_config in enumerate(config.levels):
            if first == True:
                seed = config.seed
                first = False
            else:
                seed = 0
            try:
                level = Level(
                        screen, clock, spritesheet, hud, pause_menu,
                        death_end_game, name_entry, level_config, index + 1, seed,
                        config.level_max_time, config, stats
                    )
            except LevelError as e:
                print(f"Error: {e}", file=sys.stderr)
                pygame.quit()
                sys.exit(1)
            level_result = level.run()
            if level_result == "quit":
                playing = False
                break
            elif level_result == "score saved":
                break
        else:
            # Only reached when no level did 'break': every level was cleared.
            if victory_screen.run(screen, clock, stats.score) == "quit":
                playing = False
            elif name_entry.run(screen, clock, stats.score,
                                config.highscore_filename) == "quit":
                playing = False

    pygame.quit()


if __name__ == "__main__":
    main()
