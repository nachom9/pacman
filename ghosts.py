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
        if color == "pink":
            self.x = (size[0] - 1) * 54 + 15
            self.y = 15
            self.prev_x = (size[0] - 1) * 54 + 15
            self.prev_y = 15
            self.direction = "left"
            self.movement = "left"
            self.cell = (size[0], 0)
        if color == "blue":
            self.x = 15
            self.y = (size[1] - 1) * 54 + 15
            self.prev_x = 15
            self.prev_y = (size[1] - 1) * 54 + 15
            self.direction = "right"
            self.movement = "right"
            self.cell = (0, size[1])
        if color == "orange":
            self.x = (size[0] - 1) * 54 + 15
            self.y = (size[1] - 1) * 54 + 15
            self.prev_x = (size[0] - 1) * 54 + 15
            self.prev_y = (size[1] - 1) * 54 + 15
            self.direction = "left"
            self.movement = "left"
            self.cell = (size[0], size[1])

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
        print (ghosts)
        return ghosts
