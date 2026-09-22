import pygame

class Pacman:
    def __init__(self, size, maze):
        self.sprites = self.get_sprites()
        self.direction = 0
        self.x = (len(maze[0]) // 2 * 54) + 15
        self.y = (len(maze) // 2 * 54) + 15
        self.prev_x = (len(maze[0]) // 2 * 54) + 15
        self.prev_y = (len(maze) // 2 * 54) + 15
        self.m_x = 0
        self.m_y = 0
        self.speed = 2
        self.movement = "left"
        self.mouth = 0
        self.mouth_name = "opened"
        self.cell = (size[0] // 2, size[1] // 2)
        self.maze = maze
        self.direction = "left"
        self.score = 0

    def get_sprites_backup(self):
        pacman_coords = {
            "right": {},
            "down": {},
            "left": {},
            "up": {}
            }
        directions = ["right", "down", "left", "up"]
        mouths = ["closed", "opened", "full"]
        x, y = 852, 5
        width, height = 34, 33

        for d in directions:
            for m in mouths:
                pacman_coords[d][m] = [x, y, width, height]
                y += 50

    def get_sprites(self):
        pacman_coords = {
            "right": {"rotation": 0},
            "down": {"rotation": 270},
            "left": {"rotation": 180},
            "up": {"rotation": 90},
            }
        directions = ["right", "down", "left", "up"]
        mouths = ["closed", "opened", "full"]
        x, y = 852, 5
        width, height = 34, 33

        pacman_coords["right"]["closed"] = [x, y, width, height]
        pacman_coords["right"]["opened"] = [x, y + 50, width, height]
        pacman_coords["right"]["full"] = [x, y + 100, width, height]
        pacman_coords["down"]["closed"] = [x, y, width, height]
        pacman_coords["down"]["opened"] = [x, y + 50, width, height]
        pacman_coords["down"]["full"] = [x, y + 100, width, height]
        pacman_coords["left"]["closed"] = [x, y, width, height]
        pacman_coords["left"]["opened"] = [x, y + 50, width, height]
        pacman_coords["left"]["full"] = [x, y + 100, width, height]
        pacman_coords["up"]["closed"] = [x, y, width, height]
        pacman_coords["up"]["opened"] = [x, y + 50, width, height]
        pacman_coords["up"]["full"] = [x, y + 100, width, height]

        return pacman_coords

    def predict_move(self):
        if self.direction == "left":
                self.x -= self.speed
                self.m_x -= self.speed
                self.movement = "left"
        elif self.direction == "right":
                self.x += self.speed
                self.m_x += self.speed
                self.movement = "right"
        elif self.direction == "up":
                self.y -= self.speed
                self.m_y -= self.speed
                self.movement = "up"
        elif self.direction == "down":
                self.y += self.speed
                self.m_y += self.speed
                self.movement = "down"

    def move(self, keys, drawn_maze):
        row, col = self.y // 54, self.x // 54
        self.cell = (row, col)
        c = self.maze[row][col]
        if keys[pygame.K_LEFT]:
            self.movement = "left"
        if keys[pygame.K_RIGHT]:
            self.movement = "right"
        if keys[pygame.K_UP]:
            self.movement = "up"
        if keys[pygame.K_DOWN]:
            self.movement = "down"

        if self.movement == "left":
            row, col = (self.y - 4) // 54, (self.x + 38) // 54
            row_n, col_n = (self.y + 50) // 54, (self.x + 77) // 54
            c = self.maze[row][col]
            if not (c == 8 or c == 9 or c == 10 or c == 11 or c == 12 or c == 13 or c == 14 or c == 15):
                if self.m_y % 54 == 0:
                    self.x -= self.speed
                    self.m_x -= self.speed
                    self.direction = "left"
                    if drawn_maze.cells_gums[(row_n, col_n)]:
                        self.score += 20
                        drawn_maze.cells_gums[(row_n, col_n)] = False
                        print(self.score)
                else:
                    self.predict_move()
        elif self.movement == "right":
            row, col = (self.y - 4) // 54, (self.x - 14) // 54
            row_n, col_n = (self.y + 50) // 54, (self.x + 50) // 54
            c = self.maze[row][col]
            if not (c == 2 or c == 3 or c == 6 or c == 7 or c == 10 or c == 11 or c == 14 or c == 15):
                if self.m_y % 54 == 0:
                    self.x += self.speed
                    self.m_x += self.speed
                    self.direction = "right"
                    if drawn_maze.cells_gums[(row_n, col_n)]:
                        self.score += 20
                        drawn_maze.cells_gums[(row_n, col_n)] = False
                        print(self.score)
                else:
                    self.predict_move()
        elif self.movement == "up":
            row, col = (self.y + 37) // 54, (self.x - 4) // 54
            row_n, col_n = (self.y + 77) // 54, (self.x + 50) // 54
            c = self.maze[row][col]
            if not (c == 1 or c == 3 or c == 5 or c == 7 or c == 9 or c == 11 or c == 13 or c == 15):
                if self.m_x % 54 == 0:
                    self.y -= self.speed
                    self.m_y -= self.speed
                    self.direction = "up"
                    if drawn_maze.cells_gums[(row_n, col_n)]:
                        self.score += 20
                        drawn_maze.cells_gums[(row_n, col_n)] = False
                        print(self.score)
                else:
                    self.predict_move()
        elif self.movement == "down":
            row, col = (self.y - 14) // 54, (self.x - 4) // 54
            row_n, col_n = (self.y + 50) // 54, (self.x + 50) // 54
            c = self.maze[row][col]
            if not (c == 4 or c == 5 or c == 6 or c == 7 or c == 12 or c == 13 or c == 14 or c == 15):
                if self.m_x % 54 == 0:
                    self.y += self.speed
                    self.m_y += self.speed
                    self.direction = "down"
                    if drawn_maze.cells_gums[(row_n, col_n)]:
                        self.score += 20
                        drawn_maze.cells_gums[(row_n, col_n)] = False
                        print(self.score)
                else:
                    self.predict_move()

    def change_animation(self):
        self.prev_x = self.x
        self.prev_y = self.y
        mouths = ["opened", "full", "opened", "closed"]

        if self.mouth == 3:
            self.mouth = 0
        else:
            self.mouth += 1

        self.mouth_name = mouths[self.mouth]
