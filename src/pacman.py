"""The player: movement, eating pacgums, death animation and respawn."""

from typing import TYPE_CHECKING, Any, Sequence

import pygame

from src.draw_maze import DrawnMaze
from src.game_stats import GameStats


# Sirve para ver los tipos, el if solo hace el import para comprobar tipos.
if TYPE_CHECKING:
    from src.ghosts import Ghost

CELL_SIZE = 54
CENTER_OFFSET = 15


def find_spawn_cell(maze: list[list[int]]) -> tuple[int, int]:
    """Return the (row, col) closest to the center that is not a closed cell.

    The maze generator draws a '42' of closed cells (value 15) in the
    center, so the exact center cell may not be usable.
    """
    center_row, center_col = len(maze) // 2, len(maze[0]) // 2
    best_cell = (center_row, center_col)
    best_dist = None
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] != 15:
                dist = abs(row - center_row) + abs(col - center_col)
                if best_dist is None or dist < best_dist:
                    best_dist = dist
                    best_cell = (row, col)
    return best_cell


class Pacman:
    """The player character."""

    def __init__(
        self, size: tuple[int, int], maze: list[list[int]],
        walls: list[pygame.Rect], stats: GameStats,
    ) -> None:
        """Place Pac-Man on the free cell closest to the center.

        Args:
            size: Maze size in cells, as (width, height).
            maze: Maze from the generator, maze[row][col].
            walls: Rects of every wall, used for collisions.
            stats: Score, lives and cheats of the game (shared by levels).
        """
        self.stats = stats
        self.starting_cell = find_spawn_cell(maze)
        row, col = self.starting_cell
        self.x = col * CELL_SIZE + CENTER_OFFSET
        self.y = row * CELL_SIZE + CENTER_OFFSET
        self.prev_x = self.x
        self.prev_y = self.y
        self.speed = 2
        self.movement = ""
        self.mouth = 0
        self.mouth_name = "opened"
        self.cell = self.starting_cell
        self.maze = maze
        self.direction = "left"
        self.state = "playing"
        self.rect = pygame.Rect(self.x, self.y, 34, 33)
        self.death_timer = 0
        self.brave = False
        self.brave_reset = 0
        self.walls = walls

    def get_sprites(self) -> dict[str, Any]:
        """Return the position of every Pac-Man sprite in the spritesheet.

        Returns:
            For each direction, its rotation angle and a [x, y, w, h]
            rect per mouth state; "death" is the list of death frames.
        """
        pacman_coords: dict[str, Any] = {
            "right": {"rotation": 0},
            "down": {"rotation": 270},
            "left": {"rotation": 180},
            "up": {"rotation": 90},
            "death": []
        }
        x, y = 852, 5
        width, height = 34, 33

        for direction in ("right", "down", "left", "up"):
            pacman_coords[direction]["closed"] = [x, y, width, height]
            pacman_coords[direction]["opened"] = [x, y + 50, width, height]
            pacman_coords[direction]["full"] = [x, y + 100, width, height]

        x, y = 353, 10
        for _ in range(11):
            pacman_coords["death"].append([x, y, width, height])
            y += 50

        return pacman_coords

    def predict_move(self) -> None:
        """Keep moving in the current direction (used to finish a turn)."""
        if self.direction == "left":
            self.x -= self.speed
            self.movement = "left"
        elif self.direction == "right":
            self.x += self.speed
            self.movement = "right"
        elif self.direction == "up":
            self.y -= self.speed
            self.movement = "up"
        elif self.direction == "down":
            self.y += self.speed
            self.movement = "down"

    def check_wall_collision(self, direction: str) -> bool:
        """Return True if moving 7 px in that direction would hit a wall."""
        test_rect = self.rect.copy()

        if direction == "left":
            test_rect.x -= 7

        elif direction == "right":
            test_rect.x += 7

        elif direction == "up":
            test_rect.y -= 7

        elif direction == "down":
            test_rect.y += 7

        for wall in self.walls:
            if test_rect.colliderect(wall):
                return True

        return False

    def reset_ghosts(self, ghosts: list["Ghost"]) -> None:
        """Make every ghost that is not eaten flee (super-pacgum eaten)."""
        for ghost in ghosts:
            if (ghost.mode == "chase" or
                    ghost.mode == "flee"):
                ghost.mode = 'flee'
                ghost.flee_timer = 0
                ghost.fleeing = 'blue'

    def move(
        self, keys: Sequence[bool], drawn_maze: DrawnMaze,
        ghosts: list["Ghost"], points_per_pacgum: int,
        points_per_super_pacgum: int,
    ) -> None:
        """Move Pac-Man one step according to the arrow keys.

        Pac-Man can only turn when it is aligned with a corridor; until
        then it keeps going in its current direction. A pacgum in a corner
        is a super-pacgum: it gives more points and makes the ghosts flee.

        Args:
            keys: State of the keyboard (pygame.key.get_pressed()).
            drawn_maze: Maze with the pacgums.
            ghosts: The ghosts of the level.
            points_per_pacgum: Points for a normal pacgum.
            points_per_super_pacgum: Points for a super-pacgum.
        """
        if self.brave_reset >= 4:
            self.brave_reset = 0
            self.brave = False
            for ghost in ghosts:
                if ghost.mode == 'flee':
                    ghost.mode = "chase"
        margin = CENTER_OFFSET
        row, col = ((self.y + CENTER_OFFSET) // CELL_SIZE,
                    (self.x + CENTER_OFFSET) // CELL_SIZE)
        self.cell = (row, col)

        if keys[pygame.K_LEFT]:
            self.movement = "left"
        if keys[pygame.K_RIGHT]:
            self.movement = "right"
        if keys[pygame.K_UP]:
            self.movement = "up"
        if keys[pygame.K_DOWN]:
            self.movement = "down"

        if self.movement == "left":
            if not self.check_wall_collision(self.movement):
                if (self.y - margin) % CELL_SIZE == 0:
                    self.x -= self.speed
                    self.direction = "left"

                    if drawn_maze.cells_gums[(row, col)]:
                        if ((self.cell[0] == 0 and self.cell[1] == 0) or
                                (self.cell[0] == 0 and
                                 self.cell[1] == len(self.maze[1]) - 1) or
                                (self.cell[0] == len(self.maze) - 1 and
                                 self.cell[1] == 0) or
                                (self.cell[0] == len(self.maze) - 1 and
                                 self.cell[1] == len(self.maze[1]) - 1)):
                            self.stats.score += points_per_super_pacgum
                            self.brave = True
                            self.reset_ghosts(ghosts)
                        else:
                            self.stats.score += points_per_pacgum
                        drawn_maze.cells_gums[(row, col)] = False
                else:
                    self.predict_move()
            else:
                self.movement = self.direction

        elif self.movement == "right":
            if not self.check_wall_collision(self.movement):
                if (self.y - margin) % CELL_SIZE == 0:
                    self.x += self.speed
                    self.direction = "right"

                    if drawn_maze.cells_gums[(row, col)]:
                        if ((self.cell[0] == 0 and self.cell[1] == 0) or
                                (self.cell[0] == 0 and
                                 self.cell[1] == len(self.maze[1]) - 1) or
                                (self.cell[0] == len(self.maze) - 1 and
                                 self.cell[1] == 0) or
                                (self.cell[0] == len(self.maze) - 1 and
                                 self.cell[1] == len(self.maze[1]) - 1)):
                            self.stats.score += points_per_super_pacgum
                            self.brave = True
                            self.reset_ghosts(ghosts)
                        else:
                            self.stats.score += points_per_pacgum
                        drawn_maze.cells_gums[(row, col)] = False
                else:
                    self.predict_move()
            else:
                self.movement = self.direction

        elif self.movement == "up":
            if not self.check_wall_collision(self.movement):
                if (self.x - margin) % CELL_SIZE == 0:
                    self.y -= self.speed
                    self.direction = "up"

                    if drawn_maze.cells_gums[(row, col)]:
                        if ((self.cell[0] == 0 and self.cell[1] == 0) or
                                (self.cell[0] == 0 and
                                 self.cell[1] == len(self.maze[1]) - 1) or
                                (self.cell[0] == len(self.maze) - 1 and
                                 self.cell[1] == 0) or
                                (self.cell[0] == len(self.maze) - 1 and
                                 self.cell[1] == len(self.maze[1]) - 1)):
                            self.stats.score += points_per_super_pacgum
                            self.brave = True
                            self.reset_ghosts(ghosts)
                        else:
                            self.stats.score += points_per_pacgum
                        drawn_maze.cells_gums[(row, col)] = False
                else:
                    self.predict_move()
            else:
                self.movement = self.direction

        elif self.movement == "down":
            if not self.check_wall_collision(self.movement):
                if (self.x - margin) % CELL_SIZE == 0:
                    self.y += self.speed
                    self.direction = "down"

                    if drawn_maze.cells_gums[(row, col)]:
                        if ((self.cell[0] == 0 and self.cell[1] == 0) or
                                (self.cell[0] == 0 and
                                 self.cell[1] == len(self.maze[1]) - 1) or
                                (self.cell[0] == len(self.maze) - 1 and
                                 self.cell[1] == 0) or
                                (self.cell[0] == len(self.maze) - 1 and
                                 self.cell[1] == len(self.maze[1]) - 1)):
                            self.stats.score += points_per_super_pacgum
                            self.brave = True
                            self.reset_ghosts(ghosts)
                        else:
                            self.stats.score += points_per_pacgum
                        drawn_maze.cells_gums[(row, col)] = False
                else:
                    self.predict_move()
            else:
                self.movement = self.direction

        self.rect.x = self.x
        self.rect.y = self.y

    def change_animation(self) -> None:
        """Go to the next mouth sprite (opened, full, opened, closed)."""
        self.prev_x = self.x
        self.prev_y = self.y
        mouths = ["opened", "full", "opened", "closed"]

        if self.mouth == 3:
            self.mouth = 0
        else:
            self.mouth += 1

        self.mouth_name = mouths[self.mouth]

    def death_animation(
        self, sprites: list[list[int]], clock: int
    ) -> list[int]:
        """Return the death frame for the time spent dying.

        After 1.2 seconds the state becomes "death", so the level can take
        a life away.

        Args:
            sprites: The death frames, as [x, y, w, h] rects.
            clock: Milliseconds since the last frame.

        Returns:
            The rect of the frame to draw.
        """
        if self.death_timer < 100:
            frame = sprites[0]
        elif self.death_timer < 200:
            frame = sprites[1]
        elif self.death_timer < 300:
            frame = sprites[2]
        elif self.death_timer < 400:
            frame = sprites[3]
        elif self.death_timer < 500:
            frame = sprites[4]
        elif self.death_timer < 600:
            frame = sprites[5]
        elif self.death_timer < 700:
            frame = sprites[6]
        elif self.death_timer < 800:
            frame = sprites[8]
        elif self.death_timer < 900:
            frame = sprites[9]
        elif self.death_timer < 1200:
            frame = sprites[10]
        else:
            # 'else' (not '< 1300'): a slow frame can jump over 1300 ms.
            frame = sprites[10]
            self.state = "death"

        self.death_timer += clock
        return frame

    def reset_round(
        self, ghosts: list["Ghost"], maze: list[list[int]]
    ) -> None:
        """Take a life away and put Pac-Man and the ghosts back at start."""
        size = (len(maze[0]), len(maze))
        self.stats.lives -= 1
        row, col = self.starting_cell
        self.x = col * CELL_SIZE + CENTER_OFFSET
        self.y = row * CELL_SIZE + CENTER_OFFSET
        self.prev_x = self.x
        self.prev_y = self.y
        self.movement = ""
        self.mouth = 0
        self.mouth_name = "opened"
        self.cell = self.starting_cell
        self.direction = "left"
        self.state = "playing"
        self.rect = pygame.Rect(self.x, self.y, 34, 33)
        self.death_timer = 0

        for ghost in ghosts:
            if ghost.color == "red":
                ghost.x = CENTER_OFFSET
                ghost.y = CENTER_OFFSET
                ghost.prev_x = CENTER_OFFSET
                ghost.prev_y = CENTER_OFFSET
                ghost.direction = "right"
                ghost.movement = "right"
            elif ghost.color == "pink":
                ghost.x = (size[0] - 1) * CELL_SIZE + CENTER_OFFSET
                ghost.y = CENTER_OFFSET
                ghost.prev_x = (size[0] - 1) * CELL_SIZE + CENTER_OFFSET
                ghost.prev_y = CENTER_OFFSET
                ghost.direction = "left"
                ghost.movement = "left"
            elif ghost.color == "blue":
                ghost.x = CENTER_OFFSET
                ghost.y = (size[1] - 1) * CELL_SIZE + CENTER_OFFSET
                ghost.prev_x = CENTER_OFFSET
                ghost.prev_y = (size[1] - 1) * CELL_SIZE + CENTER_OFFSET
                ghost.direction = "right"
                ghost.movement = "right"
            elif ghost.color == "orange":
                ghost.x = (size[0] - 1) * CELL_SIZE + CENTER_OFFSET
                ghost.y = (size[1] - 1) * CELL_SIZE + CENTER_OFFSET
                ghost.prev_x = (size[0] - 1) * CELL_SIZE + CENTER_OFFSET
                ghost.prev_y = (size[1] - 1) * CELL_SIZE + CENTER_OFFSET
                ghost.direction = "left"
                ghost.movement = "left"

            ghost.cell = ghost.starting_cell
            ghost.frame = '0'
            ghost.rect = pygame.Rect(ghost.x, ghost.y, 34, 33)
            ghost.mode = "chase"

    def change_cheat_mode(self) -> None:
        """Turn the cheat mode on or off."""
        if not self.stats.cheat_mode:
            self.stats.cheat_mode = True
        else:
            self.stats.cheat_mode = False
