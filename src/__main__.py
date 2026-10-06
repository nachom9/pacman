#!/usr/bin/env python3

from mazegenerator import MazeGenerator
from src.pacman import Pacman
from src.ghosts import Ghost
from src.draw_maze import DrawnMaze
from src.hud import HUD
from src.main_menu import MainMenu
from src.pause_menu import PauseMenu
from src.level_time import Time
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
    ghosts = [
        Ghost(size, maze, "red"),
        Ghost(size, maze, "pink"),
        Ghost(size, maze, "blue"),
        Ghost(size, maze, "orange")
    ]

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
    menu = MainMenu(screen.get_width(), screen.get_height())
    if menu.run(screen, clock) == "quit":
        pygame.quit()
        return
    pause_menu = PauseMenu(screen.get_width(), screen.get_height())
    running = True

    pacman_sprites = pacman.get_sprites()
    ghosts_sprites = Ghost.get_sprites()
    spritesheet = pygame.image.load("assets/sprites.png").convert_alpha()

    map_surface = drawn_maze.draw_map()

    hud = HUD(screen.get_width(), screen.get_height(), spritesheet)
    time = Time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_start = pygame.time.get_ticks()
                    if pause_menu.run(screen, clock) == "quit":
                        running = False
                        break
                    pause_duration = pygame.time.get_ticks() - pause_start
                    time.pause(pause_duration)

        if pacman.state == "playing":
            keys = pygame.key.get_pressed()
            pacman.move(keys, drawn_maze)
            for ghost in ghosts:
                ghost.set_behaviour(drawn_maze, pacman, pacman.movement, ghosts[0].cell)
                ghost.surface = spritesheet.subsurface(pygame.Rect(ghosts_sprites[ghost.color][ghost.direction][ghost.frame]))
            if abs((pacman.prev_x - pacman.x)) + abs((pacman.prev_y - pacman.y)) > 4:
                pacman.change_animation()
            pacman_surface = pygame.transform.rotate(
                spritesheet.subsurface(pygame.Rect(pacman_sprites[pacman.direction][pacman.mouth_name])),
                pacman_sprites[pacman.direction]["rotation"])

        elif pacman.state == "dying":
            death_frame = pacman.death_animation(pacman_sprites['death'], clock)
            pacman_surface = spritesheet.subsurface(pygame.Rect(death_frame))
        elif pacman.state == "death":
            pacman.reset_round(ghosts, maze)

        screen.fill((0, 0, 0))

        screen.blit(map_surface, (0, top_space))
        pacgums_surface = drawn_maze.draw_pacgums()
        screen.blit(pacgums_surface, (0, top_space))
        for ghost in ghosts:
            screen.blit(
                ghost.surface,
                (ghost.x, ghost.y + top_space)
            )

        screen.blit(
            pacman_surface,
            (pacman.x, pacman.y + top_space)
        )

        hud.draw_score(screen, pacman.score)
        hud.draw_lives(screen, pacman.lives)
        hud.draw_level(screen, 7)
        hud.draw_time(screen, time.get_elapsed_time(), 120)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
