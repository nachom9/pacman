import pygame

class Ghost:
    def __init__(self, size, maze, color, walls):
        if color == "red":
            self.starting_cell = (0, 0)
            self.x = 15
            self.y = 15
            self.prev_x = 15
            self.prev_y = 15
            self.direction = "right"
            self.movement = "right"
            self.cell = (0, 0)

        elif color == "pink":
            self.starting_cell = (0, size[0] - 1)
            self.x = (size[0] - 1) * 54 + 15
            self.y = 15
            self.prev_x = (size[0] - 1) * 54 + 15
            self.prev_y = 15
            self.direction = "left"
            self.movement = "left"
            self.cell = (0, size[0] - 1)

        elif color == "blue":
            self.starting_cell = (size[1] - 1, 0)
            self.x = 15
            self.y = (size[1] - 1) * 54 + 15
            self.prev_x = 15
            self.prev_y = (size[1] - 1) * 54 + 15
            self.direction = "right"
            self.movement = "right"
            self.cell = (size[1] - 1, 0)

        elif color == "orange":
            self.starting_cell = (size[1] - 1, size[0] - 1)
            self.x = (size[0] - 1) * 54 + 15
            self.y = (size[1] - 1) * 54 + 15
            self.prev_x = (size[0] - 1) * 54 + 15
            self.prev_y = (size[1] - 1) * 54 + 15
            self.direction = "left"
            self.movement = "left"
            self.cell = (size[1] - 1, size[0] - 1)

        self.color = color
        self.speed = 2
        self.frame = '0'
        self.maze = maze
        self.rect = pygame.Rect(self.x, self.y, 34, 33)
        self.sprites = []
        self.fleeing = "blue"
        self.flee_timer = 0
        self.walls = walls

    @staticmethod
    def get_sprites():
        ghosts = {
            "red": {
                "right": {},
                "down": {},
                "left": {},
                "up": {}
            },
            "pink": {
                "right": {},
                "down": {},
                "left": {},
                "up": {}
            },
            "blue": {
                "right": {},
                "down": {},
                "left": {},
                "up": {}
            },
            "orange": {
                "right": {},
                "down": {},
                "left": {},
                "up": {}
            },
            "fleeing": {
                "blue": {},
                "grey": {},
            }
        }

        directions = ["right", "down", "left", "up"]
        frames = ['0', '1']
        x, y = 1, 4
        width, height = 35, 35

        for ghost in ghosts.keys():
            if ghost == "fleeing":
                x = 1
                y = 554
                ghosts[ghost]['blue']['0'] = [x, y, width, height]
                y += 50
                ghosts[ghost]['blue']['1'] = [x, y, width, height]
                x += 50
                y -= 50
                ghosts[ghost]['grey']['0'] = [x, y, width, height]
                y += 50
                ghosts[ghost]['grey']['1'] = [x, y, width, height]
            else:
                for direction in directions:
                    for frame in frames:
                        ghosts[ghost][direction][frame] = [x, y, width, height]
                        y += 50
                y = 4
                x += +50
        return ghosts

    def set_behaviour(self, pacman, direction, red_ghost_cell, clock):
        if not pacman.movement:
            return
        if pacman.brave:
            self.flee(clock, pacman)
            return
        else:
            self.speed = 2
            print(
                self.color,
                "RETURN NORMAL:",
                self.x,
                self.y,
                "MOD:",
                (self.x - 15) % 54,
                (self.y - 15) % 54,
                "CELL:",
                self.cell
            )
        if pacman.rect.colliderect(self.rect):
            pacman.state = "dying"
        if self.color == 'red':
            target_cell = pacman.cell

        elif self.color == 'pink':
            if direction == "right":
                col = min(len(self.maze[1]) - 1, pacman.cell[1] + 4)
                row = pacman.cell[0]
            elif direction == "down":
                row = min(len(self.maze[0]) - 1, pacman.cell[0] + 4)
                col = pacman.cell[1]
            elif direction == "left":
                col = max(0, pacman.cell[1] - 4)
                row = pacman.cell[0]
            elif direction == "up":
                row = max(0, pacman.cell[0] - 4)
                col = pacman.cell[1]
            while self.maze[row][col] == 15:
                row += 1
                col += 1
            target_cell = (row, col)

        elif self.color == 'orange':
            if abs((self.cell[0] - pacman.cell[0])) + abs((self.cell[1] - pacman.cell[1])) < 4:
                target_cell = pacman.cell
            else:
                if direction == "left":
                    col = min(len(self.maze[1]) - 1, pacman.cell[1] + 4)
                    row = pacman.cell[0]
                elif direction == "up":
                    row = min(len(self.maze[0]) - 1, pacman.cell[0] + 4)
                    col = pacman.cell[1]
                elif direction == "right":
                    col = max(0, pacman.cell[1] - 4)
                    row = pacman.cell[0]
                elif direction == "down":
                    row = max(0, pacman.cell[0] - 4)
                    col = pacman.cell[1]
                while self.maze[row][col] == 15:
                    row += 1
                    col += 1
                target_cell = (row, col)

        elif self.color == 'blue':
            if direction == "right":
                v_col = min(len(self.maze[1]) - 1, pacman.cell[1] + 2)
                v_row = pacman.cell[0]
            elif direction == "down":
                v_row = min(len(self.maze[0]) - 1, pacman.cell[0] + 2)
                v_col = pacman.cell[1]
            elif direction == "left":
                v_col = max(0, pacman.cell[1] - 2)
                v_row = pacman.cell[0]
            elif direction == "up":
                v_row = max(0, pacman.cell[0] - 2)
                v_col = pacman.cell[1]

            row_diff = v_row - red_ghost_cell[0]
            col_diff = v_col - red_ghost_cell[1]
            row = v_row - row_diff * 2
            col = v_col - col_diff * 2

            while row >= len(self.maze[0]):
                row -= 1
            while col >= len(self.maze[1]):
                col -= 1
            while row < 0:
                row += 1
            while col < 0:
                col += 1
            while self.maze[row][col] == 15:
                row += 1
                col += 1

            target_cell = (row, col)

        self.move(target_cell)

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
        self.rect.x = self.x
        self.rect.y = self.y

    def move(self, target_cell):
        if abs((self.prev_x - self.x)) + abs((self.prev_y - self.y)) > 4:
            self.change_animation()

        row, col = self.y // 54, self.x // 54
        self.cell = (row, col)
        next_step = self.path_finding(target_cell)

        if next_step == "left":
            self.movement = "left"
            if (self.y - 15) % 54 != 0:
                self.predict_move()
                return
        if next_step == "right":
            self.movement = "right"
            if (self.y - 15) % 54 != 0:
                self.predict_move()
                return
        if next_step == "up":
            self.movement = "up"
            if (self.x - 15) % 54 != 0:
                self.predict_move()
                return
        if next_step == "down":
            self.movement = "down"
            if (self.x - 15) % 54 != 0:
                self.predict_move()
                return

        if (self.movement == "left" and
                not self.check_wall_collision(self.movement)):
            if (self.y - 15) % 54 == 0:
                self.x -= self.speed
                self.direction = "left"
            else:
                self.predict_move()

        elif (self.movement == "right" and
            not self.check_wall_collision(self.movement)):
            if (self.y - 15) % 54 == 0:
                self.x += self.speed
                self.direction = "right"
            else:
                self.predict_move()

        elif (self.movement == "up" and
            not self.check_wall_collision(self.movement)):
            if (self.x - 15) % 54 == 0:
                self.y -= self.speed
                self.direction = "up"
            else:
                self.predict_move()

        elif (self.movement == "down" and
            not self.check_wall_collision(self.movement)):
            if (self.x - 15) % 54 == 0:
                self.y += self.speed
                self.direction = "down"
            else:
                self.predict_move()

        self.rect.x = self.x
        self.rect.y = self.y

    @staticmethod
    def get_neighbors(current, c):
        neighbors = []
        row, col = current

        if not (c & 8) and col > 0:
            neighbors.append([
                (row, col - 1),
                "left"
            ])

        if not (c & 2) and col < 14:
            neighbors.append([
                (row, col + 1),
                "right"
            ])

        if not (c & 1) and row > 0:
            neighbors.append([
                (row - 1, col),
                "up"
            ])

        if not (c & 4) and row < 14:
            neighbors.append([
                (row + 1, col),
                "down"
            ])

        return neighbors

    def path_finding(self, target_cell):
        if self.cell == target_cell:
            return None
        visited = {self.cell: None}
        queue = [self.cell]

        while queue:
            current = queue.pop(0)

            if current == target_cell:
                break

            row, col = current
            c = self.maze[row][col]
            neighbors = self.get_neighbors(current, c)

            for neighbor, step in neighbors:
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited[neighbor] = [current, step]

        if target_cell not in visited:
            return None

        path = []
        steps = []
        current = target_cell

        while current != self.cell:
            previous, step = visited[current]
            path.append(current)
            steps.append(step)
            current = previous

        path.append(self.cell)
        path.reverse()
        steps.reverse()

        if steps:
            return steps[0]

        return None


    def change_animation(self):
        self.prev_x = self.x
        self.prev_y = self.y

        if self.frame == '0':
            self.frame = '1'
        else:
            self.frame = '0'

    def flee(self, clock, pacman):
        self.speed = 1
        self.move(self.starting_cell)
        self.flee_timer += clock
        if 3750 <= self.flee_timer < 4000:
            self.fleeing = "grey"
        if 4000 <= self.flee_timer < 4250:
            self.fleeing = "blue"
        if 4250 <= self.flee_timer < 4500:
            self.fleeing = "grey"
        if 4500 <= self.flee_timer < 4750:
            self.fleeing = "grey"
        if 4750 <= self.flee_timer < 5000:
            self.fleeing = "blue"
        if 5000 <= self.flee_timer < 5250:
            self.fleeing = "grey"
        if 5250 <= self.flee_timer < 5500:
            self.fleeing = "blue"
        if 5500 <= self.flee_timer < 5750:
            self.fleeing = "grey"
        if 5750 <= self.flee_timer < 6000:
            self.fleeing = "blue"
        if self.flee_timer >= 6000:
            self.fix_coords()
            self.flee_timer = 0
            pacman.brave_reset += 1

    def fix_coords(self):
        if self.x % 2 == 0:
            if self.x < 771:
                self.x += 1
            else:
                self.x -= 1

        if self.y % 2 == 0:
            if self.y < 771:
                self.y += 1
            else:
                self.y -= 1

        self.rect.x = self.x
        self.rect.y = self.y



    def flee_move(self, target_cell):

        if abs((self.prev_x - self.x)) + abs((self.prev_y - self.y)) > 4:
            self.change_animation()

        row, col = self.y // 54, self.x // 54
        self.cell = (row, col)
        next_step = self.path_finding(target_cell)
        c = self.maze[row][col]

        if next_step == "left":
            self.movement = "left"
            if (self.y - 15) % 54 != 0:
                self.predict_move()
                return
        if next_step == "right":
            self.movement = "right"
            if (self.y - 15) % 54 != 0:
                self.predict_move()
                return
        if next_step == "up":
            self.movement = "up"
            if (self.x - 15) % 54 != 0:
                self.predict_move()
                return
        if next_step == "down":
            self.movement = "down"
            if (self.x - 15) % 54 != 0:
                self.predict_move()
                return

        if self.movement == "left":
            row, col = (self.y - 4) // 54, (self.x + 38) // 54
            c = self.maze[row][col]
            if not (c == 8 or c == 9 or c == 10 or c == 11 or c == 12 or c == 13 or c == 14 or c == 15):
                if (self.y - 15) % 54 == 0:
                    self.x -= self.speed
                    self.direction = "left"
                else:
                    self.predict_move()
        elif self.movement == "right":
            row, col = (self.y - 4) // 54, (self.x - 14) // 54
            c = self.maze[row][col]
            if not (c == 2 or c == 3 or c == 6 or c == 7 or c == 10 or c == 11 or c == 14 or c == 15):
                if (self.y - 15) % 54 == 0:
                    self.x += self.speed
                    self.direction = "right"
                else:
                    self.predict_move()
        elif self.movement == "up":
            row, col = (self.y + 37) // 54, (self.x - 4) // 54
            c = self.maze[row][col]
            if not (c == 1 or c == 3 or c == 5 or c == 7 or c == 9 or c == 11 or c == 13 or c == 15):
                if (self.x - 15) % 54 == 0:
                    self.y -= self.speed
                    self.direction = "up"
                else:
                    self.predict_move()
        elif self.movement == "down":
            row, col = (self.y - 14) // 54, (self.x - 4) // 54
            c = self.maze[row][col]
            if not (c == 4 or c == 5 or c == 6 or c == 7 or c == 12 or c == 13 or c == 14 or c == 15):
                if (self.x - 15) % 54 == 0:
                    self.y += self.speed
                    self.direction = "down"
                else:
                    self.predict_move()
        self.rect.x = self.x
        self.rect.y = self.y
