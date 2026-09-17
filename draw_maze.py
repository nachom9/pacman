from mazegenerator import MazeGenerator
import pygame

class DrawnMaze:

    def __init__(self, size, cells):
        self.size = size
        self.cells = cells

    def draw_maze(self):
        maze_surface = pygame.Surface((self.size[0] * 54, self.size[1] * 54))
        x, y = 0, 0
        for row in self.cells:
            for col in row:
                c = col
                if c == 1 or c == 3 or c == 5 or c == 7 or c == 9 or c == 11 or c == 13 or c == 15:
                    pygame.draw.line(maze_surface, (33, 33, 222), (x, y), (x + 54, y), 10)
                if c == 2 or c == 3 or c == 6 or c == 7 or c == 10 or c == 11 or c == 14 or c == 15:
                    pygame.draw.line(maze_surface, (33, 33, 222), (x + 54, y), (x + 54, y + 54), 10)
                if c == 4 or c == 5 or c == 6 or c == 7 or c == 12 or c == 13 or c == 14 or c == 15:
                    pygame.draw.line(maze_surface, (33, 33, 222), (x, y + 54), (x + 54, y + 54), 10)
                if c == 8 or c == 9 or c == 10 or c == 11 or c == 12 or c == 13 or c == 14 or c == 15:
                    pygame.draw.line(maze_surface, (33, 33, 222), (x, y), (x, y + 54), 10)
                x += 54
            x = 0
            y += 54

        return maze_surface

