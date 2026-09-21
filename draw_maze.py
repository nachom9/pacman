from mazegenerator import MazeGenerator
import pygame

class DrawnMaze:

    def __init__(self, size, cells):
        self.size = size
        self.cells = cells

    def draw_maze(self):
        z = 9
        a = 4
        maze_surface = pygame.Surface((self.size[0] * 54, self.size[1] * 54))
        x, y = 0, 0
        for row in self.cells:
            for col in row:
                c = col
                if c == 1 or c == 3 or c == 5 or c == 7 or c == 9 or c == 11 or c == 13 or c == 15:
                    pygame.draw.line(maze_surface, (33, 33, 222), (x, y + 5), (x + 54, y + 5), 1)
                if c == 2 or c == 3 or c == 6 or c == 7 or c == 10 or c == 11 or c == 14 or c == 15:
                    pygame.draw.line(maze_surface, (33, 33, 222), (x + 50, y), (x + 50, y + 54), 1)
                if c == 4 or c == 5 or c == 6 or c == 7 or c == 12 or c == 13 or c == 14 or c == 15:
                    pygame.draw.line(maze_surface, (33, 33, 222), (x, y + 50), (x + 54, y + 50), 1)
                if c == 8 or c == 9 or c == 10 or c == 11 or c == 12 or c == 13 or c == 14 or c == 15:
                    pygame.draw.line(maze_surface, (33, 33, 222), (x + 5, y), (x + 5, y + 54), 1)
                pygame.draw.line(maze_surface, (33, 33, 222), (x - a, y - a), (x + z - a, y - a), 1)
                pygame.draw.line(maze_surface, (33, 33, 222), (x + z - a, y - a), (x + z - a, y + z - a), 1)
                pygame.draw.line(maze_surface, (33, 33, 222), (x - a, y + z - a), (x + z - a, y + z - a), 1)
                pygame.draw.line(maze_surface, (33, 33, 222), (x - a, y - a), (x - a, y + z - a), 1)
                x += 54
            x = 0
            y += 54

        return maze_surface

