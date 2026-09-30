import pygame

class Ghost:
    def __init__(self, size, maze, color):
        if color == "red":
            self.x = 15
            self.y = 15
            self.prev_x = 15
            self.prev_y = 15
            self.direction = "right"
            self.movement = "right"
            self.cell = (0, 0)
        elif color == "pink":
            self.x = (size[0] - 1) * 54 + 15
            self.y = 15
            self.prev_x = (size[0] - 1) * 54 + 15
            self.prev_y = 15
            self.direction = "left"
            self.movement = "left"
            self.cell = (size[0] - 1, 0)
        elif color == "blue":
            self.x = 15
            self.y = (size[1] - 1) * 54 + 15
            self.prev_x = 15
            self.prev_y = (size[1] - 1) * 54 + 15
            self.direction = "right"
            self.movement = "right"
            self.cell = (0, size[1] - 1)
        elif color == "orange":
            self.x = (size[0] - 1) * 54 + 15
            self.y = (size[1] - 1) * 54 + 15
            self.prev_x = (size[0] - 1) * 54 + 15
            self.prev_y = (size[1] - 1) * 54 + 15
            self.direction = "left"
            self.movement = "left"
            self.cell = (size[0] - 1, size[1] - 1)

        self.m_x = 0
        self.m_y = 0
        self.color = color
        self.speed = 2
        self.frame = '0'
        self.maze = maze

    def get_sprites(self):
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
            }
        }

        directions = ["right", "down", "left", "up"]
        frames = ['0', '1']
        x, y = 1, 4
        width, height = 35, 35

        for ghost in ghosts.keys():
            for direction in directions:
                for frame in frames:
                    ghosts[ghost][direction][frame] = [x, y, width, height]
                    y += 50
            y = 4
            x += +50

        return ghosts

    def set_behaviour(self, drawn_maze, pacman_cell, direction, red_ghost_cell):

        if self.color == 'red':
            target_cell = pacman_cell

        elif self.color == 'pink':
            if abs((self.cell[0] - pacman_cell[0])) + abs((self.cell[1] - pacman_cell[1])) < 4:
                target_cell = pacman_cell
            else:
                if direction == "right":
                    col = min(len(self.maze[1]) - 1, pacman_cell[1] + 4)
                    row = pacman_cell[0]
                elif direction == "down":
                    row = min(len(self.maze[0]) - 1, pacman_cell[0] + 4)
                    col = pacman_cell[0]
                elif direction == "left":
                    col = max(0, pacman_cell[1] - 4)
                    row = pacman_cell[0]
                elif direction == "up":
                    row = max(0, pacman_cell[0] - 4)
                    col = pacman_cell[0]
                while self.maze[row][col] == 15:
                    row += 1
                    col += 1
                target_cell = (row, col)

        elif self.color == 'orange':
            if abs((self.cell[0] - pacman_cell[0])) + abs((self.cell[1] - pacman_cell[1])) < 4:
                target_cell = pacman_cell
            else:
                if direction == "left":
                    col = min(len(self.maze[1]) - 1, pacman_cell[1] + 4)
                    row = pacman_cell[0]
                elif direction == "up":
                    row = min(len(self.maze[0]) - 1, pacman_cell[0] + 4)
                    col = pacman_cell[0]
                elif direction == "right":
                    col = max(0, pacman_cell[1] - 4)
                    row = pacman_cell[0]
                elif direction == "down":
                    row = max(0, pacman_cell[0] - 4)
                    col = pacman_cell[0]
                while self.maze[row][col] == 15:
                    row += 1
                    col += 1
                target_cell = (row, col)

        elif self.color == 'blue':
            if direction == "right":
                v_col = min(len(self.maze[1]) - 1, pacman_cell[1] + 2)
                v_row = pacman_cell[0]
            elif direction == "down":
                v_row = min(len(self.maze[0]) - 1, pacman_cell[0] + 2)
                v_col = pacman_cell[0]
            elif direction == "left":
                v_col = max(0, pacman_cell[1] - 2)
                v_row = pacman_cell[0]
            elif direction == "up":
                v_row = max(0, pacman_cell[0] - 2)
                v_col = pacman_cell[0]

            row_diff = v_row - red_ghost_cell[0]
            col_diff = v_col - red_ghost_cell[1]
            row = v_row - row_diff * 2
            col = v_col - col_diff * 2
            print(row, col)
            while row >= 15:
                row -= 1
            while col >= 15:
                col -= 1
            while row < 0:
                row += 1
            while col < 0:
                col += 1
            while self.maze[row][col] == 15:
                row += 1
                col += 1

            target_cell = (row, col)


        self.move(drawn_maze, target_cell)




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

    def move(self, drawn_maze, target_cell):
        next_step = self.path_finding(target_cell, drawn_maze)
        row, col = self.y // 54, self.x // 54
        self.cell = (row, col)
        c = self.maze[row][col]
        if next_step == "left":
            self.movement = "left"
            if self.m_y % 54 != 0:
                self.predict_move()
                return
        if next_step == "right":
            self.movement = "right"
            if self.m_y % 54 != 0:
                self.predict_move()
                return
        if next_step == "up":
            self.movement = "up"
            if self.m_x % 54 != 0:
                self.predict_move()
                return
        if next_step == "down":
            self.movement = "down"
            if self.m_x % 54 != 0:
                self.predict_move()
                return

        if self.movement == "left":
            row, col = (self.y - 4) // 54, (self.x + 38) // 54
            row_n, col_n = (self.y + 50) // 54, (self.x + 77) // 54
            c = self.maze[row][col]
            if not (c == 8 or c == 9 or c == 10 or c == 11 or c == 12 or c == 13 or c == 14 or c == 15):
                if self.m_y % 54 == 0:
                    self.x -= self.speed
                    self.m_x -= self.speed
                    self.direction = "left"
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
                else:
                    self.predict_move()

    @staticmethod
    def get_neighbors(current, c):
        neighbors = []
        if c >= 0 and c <= 7:
            neighbors.append([(current[0], current[1] - 1), "left"])
        if c == 0 or c == 1 or c == 4 or c == 5 or c == 8 or c == 9 or c == 12 or c == 13:
            neighbors.append([(current[0], current[1] + 1), "right"])
        if c == 0 or c == 2 or c == 4 or c == 6 or c == 8 or c == 10 or c == 12 or c == 14:
            neighbors.append([(current[0] - 1, current[1]), "up"])
        if c == 0 or c == 1 or c == 2 or c == 3 or c == 8 or c == 9 or c == 10 or c == 11:
            neighbors.append([(current[0] + 1, current[1]), "down"])

        return neighbors

    def path_finding(self, target_cell, drawn_maze):
        visited = {}
        path = []
        steps = []
        queue = [self.cell]

        while queue:
            current = queue.pop(0)
            row, col = current
            c = self.maze[row][col]
            neighbors = self.get_neighbors(current, c)
            for neighbor, step in neighbors:
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited[neighbor] = [current, step]


        path.append(target_cell)
        next_cell = visited[target_cell][0]
        next_step = visited[target_cell][1]
        while self.cell not in path:
            temp_cell = next_cell
            steps.append(next_step)
            path.append(next_cell)
            next_cell = visited[temp_cell][0]
            next_step = visited[temp_cell][1]

        path.reverse()
        steps.reverse()

        if steps:
            return steps[0]





