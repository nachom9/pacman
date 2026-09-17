import pygame

class Pacman:
    def __init__(self, size, maze):
        self.sprites = self.get_sprites()
        self.direction = 0
        self.y = len(maze) // 2 * 54
        self.x = len(maze[0]) // 2 * 54
        self.prev_x = len(maze[0]) // 2 * 54
        self.prev_y = len(maze) // 2 * 54
        self.speed = 2
        self.movement = 0
        self.mouth = 0
        self.mouth_name = "opened"
        self.cell = (size[0] // 2, size[1] // 2)
        self.maze = maze

    def get_sprites(self):
        pacman_coords = {
            "right": {},
            "down": {},
            "left": {},
            "up": {}
            }
        directions = ["right", "down", "left", "up"]
        mouths = ["closed", "opened", "full"]
        x, y = 850, 0
        width, height = 39, 39

        for d in directions:
            for m in mouths:
                pacman_coords[d][m] = [x, y, width, height]
                y += 50

        return pacman_coords

    def move(self, keys):
        direction = "left"

        if keys[pygame.K_LEFT]:
            self.movement = 1
        if keys[pygame.K_RIGHT]:
            self.movement = 2
        if keys[pygame.K_UP]:
            self.movement = 3
        if keys[pygame.K_DOWN]:
            self.movement = 4


        if self.movement == 1:
            direction = "left"
            row, col = self.y // 54, (self.x + 54) // 54
            self.cell = (row, col)
            c = self.maze[row][col]
            if c == 8 or c == 9 or c == 10 or c == 11 or c == 12 or c == 13 or c == 14 or c == 15:
                self.x -= self.speed
        elif self.movement == 2:
            direction = "right"
            row, col = self.y // 54, self.x // 54
            self.cell = (row, col)
            c = self.maze[row][col]
            if c == 2 or c == 3 or c == 6 or c == 7 or c == 10 or c == 11 or c == 14 or c == 15:
                self.x += self.speed
        elif self.movement == 3:
            direction = "up"
            row, col = (self.y - 54) // 54, self.x // 54
            self.cell = (row, col)
            c = self.maze[row][col]
            if c == 1 or c == 3 or c == 5 or c == 7 or c == 9 or c == 11 or c == 13 or c == 15:
                self.y -= self.speed
        elif self.movement == 4:
            direction = "down"
            row, col = self.y // 54, self.x // 54
            self.cell = (row, col)
            c = self.maze[row][col]
            if c == 4 or c == 5 or c == 6 or c == 7 or c == 12 or c == 13 or c == 14 or c == 15:
                self.y += self.speed

        return direction

    def change_animation(self):
        self.prev_x = self.x
        self.prev_y = self.y
        mouths = ["opened", "full", "opened", "closed"]

        if self.mouth == 3:
            self.mouth = 0
        else:
            self.mouth += 1

        self.mouth_name = mouths[self.mouth]







