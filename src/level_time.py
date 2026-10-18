"""Timer of a level."""

import pygame


class Time:
    """Count the seconds spent in a level, without the time in pause."""

    def __init__(self) -> None:
        """Start counting from now."""
        self.start_time = pygame.time.get_ticks()

    def get_elapsed_time(self) -> int:
        """Return the whole seconds elapsed since the timer started."""
        elapsed_ms = pygame.time.get_ticks() - self.start_time
        elapsed_seconds: int = elapsed_ms // 1000
        return elapsed_seconds

    def pause(self, time_paused: int) -> None:
        """Do not count a pause.

        Args:
            time_paused: Milliseconds the game was paused.
        """
        self.start_time += time_paused
