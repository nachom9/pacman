import pygame

CELL_SIZE = 54
CENTER_OFFSET = 15


def find_spawn_cell(maze):
    """Return the (row, col) closest to the center that is not a closed cell."""
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
    def __init__(self, size, maze, walls, stats):
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
        self.sprites = []
        self.brave_reset = 0
        self.walls = walls
        self.cheat_mode = False

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

    def reset_ghosts(self, ghosts):
        for ghost in ghosts:
            if (ghost.mode == "chase" or
                ghost.mode == "flee"):
                ghost.mode = 'flee'
                ghost.flee_timer = 0
                ghost.fleeing = 'blue'

    def move(self, keys, drawn_maze, ghosts, points_per_pacgum, points_per_super_pacgum):
        if self.brave_reset >= 4:
            self.brave_reset = 0
            self.brave = False
            for ghost in ghosts:
                if ghost.mode == 'flee':
                    ghost.mode = "chase"
        margin = CENTER_OFFSET
        row, col = (self.y + CENTER_OFFSET) // CELL_SIZE, (self.x + CENTER_OFFSET) // CELL_SIZE
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

    def change_cheat_mode(self):
        if not self.cheat_mode:
            self.cheat_mode = True
        else:
            self.cheat_mode = False
