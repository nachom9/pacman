#!/usr/bin/env python3

from src.hud import HUD
from src.level import BOTTOM_SPACE, TOP_SPACE, Level, LevelError
from src.level import maze_pixel_size
from src.main_menu import MainMenu
from src.pause_menu import PauseMenu
from src.parse_entry import ConfigLoader, ConfigError, LevelConfig
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
    if menu.run(screen, clock) == "quit":
        pygame.quit()
        return

    spritesheet = pygame.image.load("assets/sprites.png").convert_alpha()
    hud = HUD(screen.get_width(), screen.get_height(), spritesheet)
    pause_menu = PauseMenu(screen.get_width(), screen.get_height())

    first = True
    for index, level_config in enumerate(config.levels):
        if first == True:
            seed = config.seed
            first = False
        else:
            seed = 0
        try:
            level = Level(
                    screen, clock, spritesheet, hud, pause_menu,
                    level_config, index + 1, seed, config.level_max_time,
                )
        except LevelError as e:
            print(f"Error: {e}", file=sys.stderr)
            pygame.quit()
            sys.exit(1)
        if level.run() == "quit":
            break

    pygame.quit()


if __name__ == "__main__":
    main()
