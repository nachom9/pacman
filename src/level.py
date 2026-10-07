"""One playable level: maze, characters, timer and the game loop."""

import pygame
from mazegenerator import MazeGenerator

from src.draw_maze import DrawnMaze
from src.ghosts import Ghost
from src.hud import HUD
from src.level_time import Time
from src.pacman import Pacman
from src.parse_entry import LevelConfig
from src.pause_menu import PauseMenu

TILE_SIZE = 54
MAZE_BORDER = 10
TOP_SPACE = 100
BOTTOM_SPACE = 60

class LevelError(Exception):
    """Custom exception for level-related errors."""

def maze_pixel_size(width: int, height: int) -> tuple[int, int]:
    """Return the size in pixels of a maze of width x height cells."""
    return width * TILE_SIZE + MAZE_BORDER, height * TILE_SIZE + MAZE_BORDER


class Level:
    """A single level of the game."""
 
    def __init__(
        self,
        screen: pygame.Surface,
        clock: pygame.time.Clock,
        spritesheet: pygame.Surface,
        hud: HUD,
        pause_menu: PauseMenu,
        level_config: LevelConfig,
        number: int,
        seed: int,
        max_time: int,
    ) -> None:
        """Generate the maze and create everything the level needs.
 
        Args:
            screen: Window surface to draw on.
            clock: Clock used to limit the frame rate.
            spritesheet: Image with all the sprites.
            hud: HUD drawn on top of the game.
            pause_menu: Menu shown when the player pauses.
            level_config: Maze size of this level.
            number: Level number shown in the HUD (starts at 1).
            seed: Maze seed. 0 means a random maze.
            max_time: Time limit of the level in seconds.
 
        Raises:
            LevelError: If the maze generator fails.
        """
        self.screen = screen
        self.clock = clock
        self.spritesheet = spritesheet
        self.hud = hud
        self.pause_menu = pause_menu
        self.number = number
        self.max_time = max_time
 
        self.size = (level_config.width, level_config.height)
        try:
            maze_obj = MazeGenerator(
                size=self.size,
                perfect=False,
                entry_cell=(0, 0),
                exit_cell=(-1, -1),
                seed=seed,
            )
        except Exception as error:
            raise LevelError(
                f"maze generator failed for level {number}: {error}"
            ) from None
        self.maze = maze_obj.maze

        self.drawn_maze = DrawnMaze(size=self.size, cells=self.maze)
        self.map_surface = self.drawn_maze.draw_map()
 
        self.pacman = Pacman(self.size, self.maze)
        self.ghosts = [
            Ghost(self.size, self.maze, "red"),
            Ghost(self.size, self.maze, "pink"),
            Ghost(self.size, self.maze, "blue"),
            Ghost(self.size, self.maze, "orange"),
        ]
        self.pacman_sprites = self.pacman.get_sprites()
        self.ghosts_sprites = Ghost.get_sprites()

        # Center the maze in the space left between the HUD bars.
        maze_w, maze_h = maze_pixel_size(self.size[0], self.size[1])
        free_h = screen.get_height() - TOP_SPACE - BOTTOM_SPACE
        self.offset_x = (screen.get_width() - maze_w) // 2
        self.offset_y = TOP_SPACE + (free_h - maze_h) // 2

    def run(self) -> None:
        """Play the level until it ends.
 
        Returns:
            "quit" if the player closed the window or quit from pause.
        """
        pacman = self.pacman
        ghosts = self.ghosts
        sheet = self.spritesheet
        time = Time()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause_start = pygame.time.get_ticks()
                        result = self.pause_menu.run(self.screen, self.clock)
                        if result == "quit":
                            return "quit"
                        time.pause(pygame.time.get_ticks() - pause_start)
 
            if pacman.state == "playing":
                keys = pygame.key.get_pressed()
                pacman.move(keys, self.drawn_maze)
                for ghost in ghosts:
                    ghost.set_behaviour(
                        self.drawn_maze, pacman, pacman.movement,
                        ghosts[0].cell,
                    )
                    sprite = self.ghosts_sprites[ghost.color][
                        ghost.direction][ghost.frame]
                    ghost.surface = sheet.subsurface(pygame.Rect(sprite))
                moved = (abs(pacman.prev_x - pacman.x)
                         + abs(pacman.prev_y - pacman.y))
                if moved > 4:
                    pacman.change_animation()
                frames = self.pacman_sprites[pacman.direction]
                pacman_surface = pygame.transform.rotate(
                    sheet.subsurface(
                        pygame.Rect(frames[pacman.mouth_name])
                    ),
                    frames["rotation"],
                )
            elif pacman.state == "dying":
                death_frame = pacman.death_animation(
                    self.pacman_sprites["death"], self.clock
                )
                pacman_surface = sheet.subsurface(pygame.Rect(death_frame))
            elif pacman.state == "death":
                pacman.reset_round(ghosts, self.maze)
 
            self._draw(pacman_surface, time.get_elapsed_time())
            pygame.display.flip()
            self.clock.tick(60)
 
    def _draw(self, pacman_surface: pygame.Surface, elapsed: int) -> None:
        """Draw the maze, the characters and the HUD on the screen."""
        ox, oy = self.offset_x, self.offset_y
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.map_surface, (ox, oy))
        self.screen.blit(self.drawn_maze.draw_pacgums(), (ox, oy))
        for ghost in self.ghosts:
            self.screen.blit(ghost.surface, (ghost.x + ox, ghost.y + oy))
        self.screen.blit(
            pacman_surface, (self.pacman.x + ox, self.pacman.y + oy)
        )
 
        self.hud.draw_score(self.screen, self.pacman.score)
        self.hud.draw_lives(self.screen, self.pacman.lives)
        self.hud.draw_level(self.screen, self.number)
        self.hud.draw_time(self.screen, elapsed, self.max_time)
