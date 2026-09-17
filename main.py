#!/usr/bin/env python3

from mazegenerator import MazeGenerator
from pacman import Pacman
from maze import Cell
from draw_maze import DrawnMaze
import pygame



def main():
    size = (15, 15)
    maze_obj = MazeGenerator(
        size=size,
        perfect=False,
        entry_cell=(0, 0),
        exit_cell=(-1, -1),
        seed=0
    )
    maze_obj.generate()
    maze = maze_obj.maze
    drawn_maze = DrawnMaze(
        size=size,
        cells=maze
    )

    pacman = Pacman(size, maze)

    pygame.init()
    screen = pygame.display.set_mode((size[0] * 54, size[1] * 54))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Pacman")
    running = True

    pacman_sprites = pacman.get_sprites()
    spritesheet = pygame.image.load("sprites.png").convert_alpha()



    maze_surface = drawn_maze.draw_maze()


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        direction = pacman.move(keys)
        if abs((pacman.prev_x - pacman.x)) + abs((pacman.prev_y - pacman.y)) > 4:
            pacman.change_animation()
        pacman_surface = spritesheet.subsurface(pygame.Rect(pacman_sprites[direction][pacman.mouth_name]))

        screen.fill((0, 0, 0))

        screen.blit(maze_surface, (0, 0))
        screen.blit(pacman_surface, (pacman.x, pacman.y))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
