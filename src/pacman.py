import pygame

class Pacman:
    def __init__(self, size, maze, walls):
        self.lives = 3
        self.x = (len(maze[0]) // 2 * 54) + 15
        self.y = (len(maze) // 2 * 54) + 15
        self.prev_x = (len(maze[0]) // 2 * 54) + 15
        self.prev_y = (len(maze) // 2 * 54) + 15
        self.speed = 2
        self.movement = ""
        self.mouth = 0
        self.mouth_name = "opened"
        self.cell = (size[0] // 2, size[1] // 2)
        self.maze = maze
        self.direction = "left"
        self.score = 0
        self.state = "playing"
        self.rect = pygame.Rect(self.x, self.y, 34, 33)
        self.death_timer = 0
        self.brave = False
        self.sprites = []
        self.brave_reset = 0
        self.walls = walls

    def get_sprites(self):
        pacman_coords = {
            "right": {"rotation": 0},
            "down": {"rotation": 270},
            "left": {"rotation": 180},
            "up": {"rotation": 90},
            "death": []
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

        x, y = 353, 10
        for _ in range (11):
            pacman_coords["death"].append([x, y, width, height])
            y += 50

        return pacman_coords

    def predict_move(self):
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

    def check_wall_collision(self, direction):
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

    @staticmethod
    def reset_ghosts(ghosts):
        for ghost in ghosts:
            ghost.mode = 'flee'
            ghost.flee_timer = 0

    def move(self, keys, drawn_maze, ghosts):
        if self.brave_reset == 4:
            self.brave_reset = 0
            self.brave = False
            for ghost in ghosts:
                ghost.mode = "chase"
        row_n, col_n = (self.y + 50) // 54, (self.x + 50) // 54
        margin = 15
        row, col = self.y // 54, self.x // 54
        self.cell = (row, col)

        if keys[pygame.K_LEFT]:
            self.movement = "left"
        if keys[pygame.K_RIGHT]:
            self.movement = "right"
        if keys[pygame.K_UP]:
            self.movement = "up"
        if keys[pygame.K_DOWN]:
            self.movement = "down"

        if (self.movement == "left" and
                not self.check_wall_collision(self.movement)):
            if (self.y - margin) % 54 == 0:
                self.x -= self.speed
                self.direction = "left"
                row_n, col_n = (self.y + 50) // 54, (self.x + 77) // 54

                if drawn_maze.cells_gums[(row_n, col_n)]:
                    if ((self.cell[0] == 0 and self.cell[1] == 0) or
                        (self.cell[0] == 0 and
                        self.cell[1] == len(self.maze[1]) - 1) or
                        (self.cell[0] == len(self.maze[0]) - 1 and
                        self.cell[1] == 0) or
                        (self.cell[0] == len(self.maze[0]) - 1 and
                        self.cell[1] == len(self.maze[1]) - 1)):
                        self.score += 50
                        self.brave = True
                        Pacman.reset_ghosts(ghosts)
                    else:
                        self.score += 10
                    drawn_maze.cells_gums[(row_n, col_n)] = False
            else:
                self.predict_move()

        elif (self.movement == "right" and
            not self.check_wall_collision(self.movement)):
            if (self.y - margin) % 54 == 0:
                row_n, col_n = (self.y + 50) // 54, (self.x + 50) // 54
                self.x += self.speed
                self.direction = "right"

                if drawn_maze.cells_gums[(row_n, col_n)]:
                    if ((self.cell[0] == 0 and self.cell[1] == 0) or
                        (self.cell[0] == 0 and
                        self.cell[1] == len(self.maze[1]) - 1) or
                        (self.cell[0] == len(self.maze[0]) - 1 and
                        self.cell[1] == 0) or
                        (self.cell[0] == len(self.maze[0]) - 1 and
                        self.cell[1] == len(self.maze[1]) - 1)):
                        self.score += 50
                        self.brave = True
                        Pacman.reset_ghosts(ghosts)
                    else:
                        self.score += 10
                    drawn_maze.cells_gums[(row_n, col_n)] = False
            else:
                self.predict_move()

        elif (self.movement == "up" and
            not self.check_wall_collision(self.movement)):
            if (self.x - margin) % 54 == 0:
                row_n, col_n = (self.y + 77) // 54, (self.x + 50) // 54
                self.y -= self.speed
                self.direction = "up"

                if drawn_maze.cells_gums[(row_n, col_n)]:
                    if ((self.cell[0] == 0 and self.cell[1] == 0) or
                        (self.cell[0] == 0 and
                        self.cell[1] == len(self.maze[1]) - 1) or
                        (self.cell[0] == len(self.maze[0]) - 1 and
                        self.cell[1] == 0) or
                        (self.cell[0] == len(self.maze[0]) - 1 and
                        self.cell[1] == len(self.maze[1]) - 1)):
                        self.score += 50
                        self.brave = True
                        Pacman.reset_ghosts(ghosts)
                    else:
                        self.score += 10
                    drawn_maze.cells_gums[(row_n, col_n)] = False
            else:
                self.predict_move()

        elif (self.movement == "down" and
            not self.check_wall_collision(self.movement)):
            if (self.x - margin) % 54 == 0:
                row_n, col_n = (self.y + 50) // 54, (self.x + 50) // 54
                self.y += self.speed
                self.direction = "down"

                if drawn_maze.cells_gums[(row_n, col_n)]:
                    if ((self.cell[0] == 0 and self.cell[1] == 0) or
                        (self.cell[0] == 0 and
                        self.cell[1] == len(self.maze[1]) - 1) or
                        (self.cell[0] == len(self.maze[0]) - 1 and
                        self.cell[1] == 0) or
                        (self.cell[0] == len(self.maze[0]) - 1 and
                        self.cell[1] == len(self.maze[1]) - 1)):
                        self.score += 50
                        self.brave = True
                        Pacman.reset_ghosts(ghosts)
                    else:
                        self.score += 10
                    drawn_maze.cells_gums[(row_n, col_n)] = False
            else:
                self.predict_move()

        self.rect.x = self.x
        self.rect.y = self.y

    def change_animation(self):
        self.prev_x = self.x
        self.prev_y = self.y
        mouths = ["opened", "full", "opened", "closed"]

        if self.mouth == 3:
            self.mouth = 0
        else:
            self.mouth += 1

        self.mouth_name = mouths[self.mouth]

    def death_animation(self, sprites, clock):
        if self.death_timer < 100:
            frame = sprites[0]
        elif self.death_timer >= 100 and self.death_timer < 200:
            frame = sprites[1]
        elif self.death_timer >= 200 and self.death_timer < 300:
            frame =  sprites[2]
        elif self.death_timer >= 300 and self.death_timer < 400:
            frame = sprites[3]
        elif self.death_timer >= 400 and self.death_timer < 500:
            frame = sprites[4]
        elif self.death_timer >= 500 and self.death_timer < 600:
            frame = sprites[5]
        elif self.death_timer >= 600 and self.death_timer < 700:
            frame = sprites[6]
        elif self.death_timer >= 700 and self.death_timer < 800:
            frame = sprites[8]
        elif self.death_timer >= 800 and self.death_timer < 900:
            frame = sprites[9]
        elif self.death_timer >= 900 and self.death_timer < 1200:
            frame = sprites[10]
        elif self.death_timer >= 1200 and self.death_timer < 1300:
            frame = sprites[10]
            self.state = "death"

        self.death_timer += clock
        return frame

    def reset_round(self, ghosts, maze):
        size = ((len(maze[0]), len(maze[1])))
        self.lives -= 1
        self.x = (len(maze[0]) // 2 * 54) + 15
        self.y = (len(maze) // 2 * 54) + 15
        self.prev_x = (len(maze[0]) // 2 * 54) + 15
        self.prev_y = (len(maze) // 2 * 54) + 15
        self.movement = "left"
        self.mouth = 0
        self.mouth_name = "opened"
        self.cell = (size[0] // 2, size[1] // 2)
        self.direction = "left"
        self.state = "playing"
        self.rect = pygame.Rect(self.x, self.y, 34, 33)
        self.death_timer = 0

        for ghost in ghosts:
            if ghost.color == "red":
                ghost.x = 15
                ghost.y = 15
                ghost.prev_x = 15
                ghost.prev_y = 15
                ghost.direction = "right"
                ghost.movement = "right"
                ghost.cell = (0, 0)
            elif ghost.color == "pink":
                ghost.x = (size[0] - 1) * 54 + 15
                ghost.y = 15
                ghost.prev_x = (size[0] - 1) * 54 + 15
                ghost.prev_y = 15
                ghost.direction = "left"
                ghost.movement = "left"
                ghost.cell = (size[0] - 1, 0)
            elif ghost.color == "blue":
                ghost.x = 15
                ghost.y = (size[1] - 1) * 54 + 15
                ghost.prev_x = 15
                ghost.prev_y = (size[1] - 1) * 54 + 15
                ghost.direction = "right"
                ghost.movement = "right"
                ghost.cell = (0, size[1] - 1)
            elif ghost.color == "orange":
                ghost.x = (size[0] - 1) * 54 + 15
                ghost.y = (size[1] - 1) * 54 + 15
                ghost.prev_x = (size[0] - 1) * 54 + 15
                ghost.prev_y = (size[1] - 1) * 54 + 15
                ghost.direction = "left"
                ghost.movement = "left"
                ghost.cell = (size[0] - 1, size[1] - 1)

            ghost.frame = '0'
            ghost.rect = pygame.Rect(ghost.x, ghost.y, 34, 33)
