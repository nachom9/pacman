"""Draw the maze walls and the pacgums, and keep track of eaten pacgums."""

import pygame

CELL_SIZE = 54
WALL_COLOR = (33, 33, 222)
PACGUM_COLOR = (222, 161, 133)


class DrawnMaze:
    """Maze drawn on a surface, with its wall rects and its pacgums."""

    def __init__(
        self, size: tuple[int, int], cells: list[list[int]]
    ) -> None:
        """Store the maze and place a pacgum in every open cell.

        Args:
            size: Maze size in cells, as (width, height).
            cells: Maze from the generator, cells[row][col]. Each cell is
                a 4-bit number: 1 = wall up, 2 = right, 4 = down, 8 = left.
        """
        self.size = size
        self.cells = cells
        self.cells_gums = self.init_pacgums()
        self.walls: list[pygame.Rect] = []
        self.color = WALL_COLOR

    def draw_map(self) -> pygame.Surface:
        """Draw every wall of the maze and remember its rect for collisions.

        Returns:
            Surface with the whole maze drawn on it.
        """
        z = 9
        a = 4
        map_surface = pygame.Surface((self.size[0] * CELL_SIZE + 10,
                                      self.size[1] * CELL_SIZE + 10))
        x, y = 4, 4

        for row in self.cells:
            for col in row:
                c = col
                if c in (1, 3, 5, 7, 9, 11, 13, 15):
                    pygame.draw.line(map_surface, self.color,
                                     (x, y + 5), (x + CELL_SIZE, y + 5), 1)
                    self.walls.append(pygame.Rect(x, y + 5, CELL_SIZE, 1))
                if c in (2, 3, 6, 7, 10, 11, 14, 15):
                    pygame.draw.line(map_surface, self.color,
                                     (x + 50, y), (x + 50, y + CELL_SIZE), 1)
                    self.walls.append(pygame.Rect(x + 50, y, 1, CELL_SIZE))
                if c in (4, 5, 6, 7, 12, 13, 14, 15):
                    pygame.draw.line(map_surface, self.color,
                                     (x, y + 50), (x + CELL_SIZE, y + 50), 1)
                    self.walls.append(pygame.Rect(x, y + 50, CELL_SIZE, 1))
                if c in (8, 9, 10, 11, 12, 13, 14, 15):
                    pygame.draw.line(map_surface, self.color,
                                     (x + 5, y), (x + 5, y + CELL_SIZE), 1)
                    self.walls.append(pygame.Rect(x + 5, y, 1, CELL_SIZE))
                pygame.draw.line(map_surface, self.color,
                                 (x - a, y - a), (x + z - a, y - a), 1)
                pygame.draw.line(map_surface, self.color,
                                 (x + z - a, y - a), (x + z - a, y + z - a), 1)
                pygame.draw.line(map_surface, self.color,
                                 (x - a, y + z - a), (x + z - a, y + z - a), 1)
                pygame.draw.line(map_surface, self.color,
                                 (x - a, y - a), (x - a, y + z - a), 1)
                x += CELL_SIZE
            x = 4
            y += CELL_SIZE
        x = CELL_SIZE * len(self.cells[0]) + 4
        y = 4
        for row in self.cells:
            pygame.draw.line(map_surface, self.color,
                             (x - a, y - a), (x + z - a, y - a), 1)
            pygame.draw.line(map_surface, self.color,
                             (x + z - a, y - a), (x + z - a, y + z - a), 1)
            pygame.draw.line(map_surface, self.color,
                             (x - a, y + z - a), (x + z - a, y + z - a), 1)
            pygame.draw.line(map_surface, self.color,
                             (x - a, y - a), (x - a, y + z - a), 1)
            y += CELL_SIZE

        x = 4
        y = CELL_SIZE * len(self.cells) + 4
        for col in range(len(self.cells[0]) + 1):
            pygame.draw.line(map_surface, self.color,
                             (x - a, y - a), (x + z - a, y - a), 1)
            pygame.draw.line(map_surface, self.color,
                             (x + z - a, y - a), (x + z - a, y + z - a), 1)
            pygame.draw.line(map_surface, self.color,
                             (x - a, y + z - a), (x + z - a, y + z - a), 1)
            pygame.draw.line(map_surface, self.color,
                             (x - a, y - a), (x - a, y + z - a), 1)
            x += CELL_SIZE

        return map_surface

    def init_pacgums(self) -> dict[tuple[int, int], bool]:
        """Put a pacgum in every cell that is not a closed '42' cell.

        Returns:
            Dict {(row, col): True} with one entry per open cell.
        """
        cells_gums: dict[tuple[int, int], bool] = {}

        for n_row, row in enumerate(self.cells):
            for n_col, col in enumerate(row):
                if col != 15:
                    cells_gums[(n_row, n_col)] = True

        return cells_gums

    def draw_pacgums(self) -> pygame.Surface:
        """Draw the pacgums not eaten yet and update win_check.

        Super-pacgums (bigger) are drawn in the 4 corners. win_check
        becomes True when no pacgum is left.

        Returns:
            Transparent surface with the pacgums drawn on it.
        """
        pacgums_surface = pygame.Surface((self.size[0] * CELL_SIZE,
                                          self.size[1] * CELL_SIZE),
                                         pygame.SRCALPHA)
        x, y = 31, 31
        # Center of the pacgums of the last column and of the last row.
        last_x = self.size[0] * CELL_SIZE + 31 - CELL_SIZE
        last_y = self.size[1] * CELL_SIZE + 31 - CELL_SIZE
        self.win_check = True

        for n_row, row in enumerate(self.cells):
            for n_col, col in enumerate(row):
                row_n, col_n = n_row, n_col
                corner = ((x == 31 and y == 31) or (x == 31 and y == last_y)
                          or (y == 31 and x == last_x)
                          or (x == last_x and y == last_y))
                if corner and self.cells_gums[(row_n, col_n)]:
                    pygame.draw.circle(pacgums_surface, PACGUM_COLOR,
                                       (x, y), 10)
                    self.win_check = False
                elif col != 15 and (self.cells_gums[(row_n, col_n)]):
                    pygame.draw.circle(pacgums_surface, PACGUM_COLOR,
                                       (x, y), 4)
                    self.win_check = False
                x += CELL_SIZE
            x = 31
            y += CELL_SIZE

        return pacgums_surface
