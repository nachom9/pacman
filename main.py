#!/usr/bin/env python3

from mazegenerator import MazeGenerator
from pacman import Pacman
from ghosts import Ghost
from draw_maze import DrawnMaze
from hud import HUD
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
    red_ghost = Ghost(size, maze, "red")
    pink_ghost = Ghost(size, maze, "pink")
    blue_ghost = Ghost(size, maze, "blue")
    orange_ghost = Ghost(size, maze, "orange")

    pygame.init()
    maze_width = size[0] * 54 + 10
    maze_height = size[1] * 54 + 10

    top_space = 100
    bottom_space = 60

    screen = pygame.display.set_mode(
        (maze_width, maze_height + top_space + bottom_space)
    )
    clock = pygame.time.Clock()
    pygame.display.set_caption("Pacman")
    running = True

    pacman_sprites = pacman.get_sprites()
    ghosts_sprites = red_ghost.get_sprites()
    spritesheet = pygame.image.load("assets/sprites.png").convert_alpha()

    map_surface = drawn_maze.draw_map()

    hud = HUD(screen.get_width(), screen.get_height(), spritesheet)
    start_time = pygame.time.get_ticks()

    print(orange_ghost.path_finding((0, 0), drawn_maze))
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
        red_ghost_surface = spritesheet.subsurface(pygame.Rect(ghosts_sprites[red_ghost.color][red_ghost.direction][red_ghost.frame]))
        pink_ghost_surface = spritesheet.subsurface(pygame.Rect(ghosts_sprites[pink_ghost.color][pink_ghost.direction][pink_ghost.frame]))
        blue_ghost_surface = spritesheet.subsurface(pygame.Rect(ghosts_sprites[blue_ghost.color][blue_ghost.direction][blue_ghost.frame]))
        orange_ghost_surface = spritesheet.subsurface(pygame.Rect(ghosts_sprites[orange_ghost.color][orange_ghost.direction][orange_ghost.frame]))

        screen.fill((0, 0, 0))


        screen.blit(map_surface, (0, top_space))
        pacgums_surface = drawn_maze.draw_pacgums()
        screen.blit(pacgums_surface, (0, top_space))
        screen.blit(
            red_ghost_surface,
            (red_ghost.x, red_ghost.y + top_space)
        )
        screen.blit(
            pink_ghost_surface,
            (pink_ghost.x, pink_ghost.y + top_space)
        )
        screen.blit(
            blue_ghost_surface,
            (blue_ghost.x, blue_ghost.y + top_space)
        )
        screen.blit(
            orange_ghost_surface,
            (orange_ghost.x, orange_ghost.y + top_space)
        )
        screen.blit(
            pacman_surface,
            (pacman.x, pacman.y + top_space)
        )

        hud.draw_score(screen, pacman.score)
        hud.draw_lives(screen, pacman.lives)
        hud.draw_level(screen, 7)
        hud.draw_time(screen, start_time, 120)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
