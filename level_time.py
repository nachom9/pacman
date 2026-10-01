import pygame


class Time:
    def __init__(self):
        self.start_time = pygame.time.get_ticks()

    def get_elapsed_time(self):
        elapsed_ms = pygame.time.get_ticks() - self.start_time
        elapsed_seconds = elapsed_ms // 1000
        return elapsed_seconds

    def pause(self, time_paused):
        self.start_time += time_paused
