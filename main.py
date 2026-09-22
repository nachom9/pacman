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
    screen = pygame.display.set_mode((size[0] * 54 + 10, size[1] * 54 + 10))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Pacman")
    running = True

    pacman_sprites = pacman.get_sprites()
    spritesheet = pygame.image.load("sprites.png").convert_alpha()



    map_surface = drawn_maze.draw_map()


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        pacman.move(keys, drawn_maze)
        if abs((pacman.prev_x - pacman.x)) + abs((pacman.prev_y - pacman.y)) > 4:
            pacman.change_animation()
        pacman_surface = pygame.transform.rotate(
            spritesheet.subsurface(pygame.Rect(pacman_sprites[pacman.direction][pacman.mouth_name])),
            pacman_sprites[pacman.direction]["rotation"])

        screen.fill((0, 0, 0))


        screen.blit(map_surface, (0, 0))
        pacgums_surface = drawn_maze.draw_pacgums()
        screen.blit(pacgums_surface, (0, 0))
        screen.blit(pacman_surface, (pacman.x, pacman.y))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
