import pygame

CELL_SIZE = 54
CENTER_OFFSET = 15

class Ghost:
    def __init__(self, size, maze, color, walls):
        if color == "red":
            self.starting_cell = (0, 0)
            self.x = CENTER_OFFSET
            self.y = CENTER_OFFSET
            self.prev_x = CENTER_OFFSET
            self.prev_y = CENTER_OFFSET
            self.direction = "right"
            self.movement = "right"
            self.cell = (0, 0)

        elif color == "pink":
            self.starting_cell = (0, size[0] - 1)
            self.x = (size[0] - 1) * CELL_SIZE + CENTER_OFFSET
            self.y = CENTER_OFFSET
            self.prev_x = (size[0] - 1) * CELL_SIZE + CENTER_OFFSET
            self.prev_y = CENTER_OFFSET
            self.direction = "left"
            self.movement = "left"
            self.cell = (0, size[0] - 1)

        elif color == "blue":
            self.starting_cell = (size[1] - 1, 0)
            self.x = CENTER_OFFSET
            self.y = (size[1] - 1) * CELL_SIZE + CENTER_OFFSET
            self.prev_x = CENTER_OFFSET
            self.prev_y = (size[1] - 1) * CELL_SIZE + CENTER_OFFSET
            self.direction = "right"
            self.movement = "right"
            self.cell = (size[1] - 1, 0)

        elif color == "orange":
            self.starting_cell = (size[1] - 1, size[0] - 1)
            self.x = (size[0] - 1) * CELL_SIZE + CENTER_OFFSET
            self.y = (size[1] - 1) * CELL_SIZE + CENTER_OFFSET
            self.prev_x = (size[0] - 1) * CELL_SIZE + CENTER_OFFSET
            self.prev_y = (size[1] - 1) * CELL_SIZE + CENTER_OFFSET
            self.direction = "left"
            self.movement = "left"
            self.cell = (size[1] - 1, size[0] - 1)

        self.maze_size = size
        self.color = color
        self.speed = 2
        self.frame = '0'
        self.maze = maze
        self.rect = pygame.Rect(self.x, self.y, 34, 33)
        self.sprites = []
        self.mode = 'chase'
        self.fleeing = "blue"
        self.flee_timer = 0
        self.eaten_timer = 0
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
            },
            "eaten":  {
                "right": {},
                "down": {},
                "left": {},
                "up": {}
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
            elif ghost == "eaten":
                x = 301
                y = 254
                for direction in directions:
                    ghosts[ghost][direction] = [x, y, width, height]
                    y += 50
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
        if self.mode == 'flee':
            if pacman.rect.colliderect(self.rect):
                self.mode = "eaten"
                return
            else:
                self.flee(clock, pacman)
            return
        if self.mode == 'eaten':
            self.eaten_flee(clock, pacman)
            return
        else:
            self.speed = 2
        if pacman.rect.colliderect(self.rect) and self.mode == "chase":
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
            while self.maze[row][col] == CENTER_OFFSET:
                row += 1
                col += 1
            target_cell = (row, col)

        elif self.color == 'orange':
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
            while self.maze[row][col] == CENTER_OFFSET:
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
            while self.maze[row][col] == CENTER_OFFSET:
                row += 1
                col += 1

            target_cell = (row, col)

        self.move(target_cell)

    def is_centered(self):
        return ((self.y - CENTER_OFFSET) % CELL_SIZE == 0 and
                (self.x - CENTER_OFFSET) % CELL_SIZE == 0)


    def move(self, target_cell):
        if abs((self.prev_x - self.x)) + abs((self.prev_y - self.y)) > 4:
            self.change_animation()

        self.cell = self.y // CELL_SIZE, self.x // CELL_SIZE

        if self.is_centered():
            next_step = self.path_finding(target_cell)
            if next_step == None:
                return
            self.movement = next_step
            self.direction = next_step

        coord = self.x if self.direction in ('left', 'right') else self.y
        rest = (coord - CENTER_OFFSET) % CELL_SIZE

        if self.direction in ("down", "right"):
            distance = (CELL_SIZE - rest) % CELL_SIZE or CELL_SIZE
            step = min(self.speed, distance)
        else:
            distance = rest or CELL_SIZE
            step = -min(self.speed, distance)

        if self.direction in ("right", "left"):
            self.x += step
        else:
            self.y += step

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

    def eaten_flee(self, clock, pacman):
        if self.eaten_timer == 0:
            self.speed = 4
            self.flee_timer = 0
            self.eaten_timer = 1
            return

        self.move(self.starting_cell)
        self.eaten_timer += clock

        if self.eaten_timer > 6000:
            self.mode = "chase"
            self.eaten_timer = 0
            pacman.brave_reset += 1

    def flee(self, clock, pacman):
        self.speed = 1
        self.move(self.starting_cell)
        self.flee_timer += clock
        if self.flee_timer < 3750:
            self.fleeing = "blue"
        if 3750 <= self.flee_timer < 4000:
            self.fleeing = "grey"
        if 4000 <= self.flee_timer < 4250:
            self.fleeing = "blue"
        if 4250 <= self.flee_timer < 4500:
            self.fleeing = "grey"
        if 4500 <= self.flee_timer < 4750:
            self.fleeing = "blue"
        if 4750 <= self.flee_timer < 5000:
            self.fleeing = "grey"
        if 5000 <= self.flee_timer < 5250:
            self.fleeing = "blue"
        if 5250 <= self.flee_timer < 5500:
            self.fleeing = "grey"
        if 5500 <= self.flee_timer < 5750:
            self.fleeing = "blue"
        if 5750 <= self.flee_timer < 6000:
            self.fleeing = "grey"
        if self.flee_timer >= 6000:
            self.flee_timer = 0
            pacman.brave_reset += 1
