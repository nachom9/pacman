from mazegenerator import MazeGenerator
import pygame

class DrawnMaze:

    def __init__(self, size, cells):
        self.size = size
        self.cells = cells
        self.cells_gums = self.init_pacgums()

    def draw_map(self):
        z = 9
        a = 4
        map_surface = pygame.Surface((self.size[0] * 54 + 9, self.size[1] * 54 + 9))
        x, y = 4, 4
        for row in self.cells:
            for col in row:
                c = col
                if c == 1 or c == 3 or c == 5 or c == 7 or c == 9 or c == 11 or c == 13 or c == 15:
                    pygame.draw.line(map_surface, (33, 33, 222), (x, y + 5), (x + 54, y + 5), 1)
                if c == 2 or c == 3 or c == 6 or c == 7 or c == 10 or c == 11 or c == 14 or c == 15:
                    pygame.draw.line(map_surface, (33, 33, 222), (x + 50, y), (x + 50, y + 54), 1)
                if c == 4 or c == 5 or c == 6 or c == 7 or c == 12 or c == 13 or c == 14 or c == 15:
                    pygame.draw.line(map_surface, (33, 33, 222), (x, y + 50), (x + 54, y + 50), 1)
                if c == 8 or c == 9 or c == 10 or c == 11 or c == 12 or c == 13 or c == 14 or c == 15:
                    pygame.draw.line(map_surface, (33, 33, 222), (x + 5, y), (x + 5, y + 54), 1)
                pygame.draw.line(map_surface, (33, 33, 222), (x - a, y - a), (x + z - a, y - a), 1)
                pygame.draw.line(map_surface, (33, 33, 222), (x + z - a, y - a), (x + z - a, y + z - a), 1)
                pygame.draw.line(map_surface, (33, 33, 222), (x - a, y + z - a), (x + z - a, y + z - a), 1)
                pygame.draw.line(map_surface, (33, 33, 222), (x - a, y - a), (x - a, y + z - a), 1)
                x += 54
                print(x)
            x = 4
            y += 54
        x = 54 * len(self.cells) + 4
        y = 4
        for row in self.cells:
            pygame.draw.line(map_surface, (33, 33, 222), (x - a, y - a), (x + z - a, y - a), 1)
            pygame.draw.line(map_surface, (33, 33, 222), (x + z - a, y - a), (x + z - a, y + z - a), 1)
            pygame.draw.line(map_surface, (33, 33, 222), (x - a, y + z - a), (x + z - a, y + z - a), 1)
            pygame.draw.line(map_surface, (33, 33, 222), (x - a, y - a), (x - a, y + z - a), 1)
            y += 54

        x = 4
        y = 54 * len(self.cells) + 4
        for col in range(len(self.cells[0]) + 1):
            pygame.draw.line(map_surface, (33, 33, 222), (x - a, y - a), (x + z - a, y - a), 1)
            pygame.draw.line(map_surface, (33, 33, 222), (x + z - a, y - a), (x + z - a, y + z - a), 1)
            pygame.draw.line(map_surface, (33, 33, 222), (x - a, y + z - a), (x + z - a, y + z - a), 1)
            pygame.draw.line(map_surface, (33, 33, 222), (x - a, y - a), (x - a, y + z - a), 1)
            x += 54

        return map_surface

    def init_pacgums(self):
        x, y = 31, 31
        cells_gums = {}

        for row in self.cells:
            for col in row:
                if col != 15:
                    row, col = (y + 31) // 54, (x + 31) // 54
                    cells_gums[(row, col)] = True
                x += 54
            x = 31
            y += 54

        return cells_gums

    def draw_pacgums(self):
        pacgums_surface = pygame.Surface((self.size[0] * 54, self.size[1] * 54), pygame.SRCALPHA)
        x, y = 31, 31

        for row in self.cells:
            for col in row:
                row_n, col_n = (y + 31) // 54, (x + 31) // 54
                if col != 15 and not (self.cells_gums[(row_n, col_n)] == False):
                    pygame.draw.circle(pacgums_surface, (222, 161, 133), (x, y), 4)
                x += 54
            x = 31
            y += 54

        return pacgums_surface
