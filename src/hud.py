"""In-game HUD: score, lives, level, time and cheat indicators."""

import pygame

from src.paths import FONT_PATH

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)


class HUD:
    """Draw the game information around the maze."""

    def __init__(
        self, screen_width: int, screen_height: int,
        spritesheet: pygame.Surface,
    ) -> None:
        """Load the fonts and the life icon.

        Args:
            screen_width: Width of the window in pixels.
            screen_height: Height of the window in pixels.
            spritesheet: Image with all the sprites.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(
            FONT_PATH,
            25
        )
        self.font_small = pygame.font.Font(
            FONT_PATH,
            18
        )
        self.lives_sprite = spritesheet.subsurface(
            pygame.Rect(595, 601, 24, 26)
        )

    def draw_score(self, screen: pygame.Surface, score: int) -> None:
        """Draw the score at the top center of the window."""
        score_label = self.font.render("SCORE", True, WHITE)
        score_value = self.font.render(str(score), True, WHITE)

        score_label_rect = score_label.get_rect()
        score_value_rect = score_value.get_rect()

        score_label_rect.center = (screen.get_width() // 2, 30)
        score_value_rect.center = (screen.get_width() // 2, 65)

        screen.blit(score_label, score_label_rect)
        screen.blit(score_value, score_value_rect)

    def draw_lives(self, screen: pygame.Surface, lives: int) -> None:
        """Draw one icon per life, or one icon and "xN" if there are > 5."""
        if lives <= 5:
            for i in range(lives):
                x = 20 + i * 40
                y = screen.get_height() - 45
                screen.blit(self.lives_sprite, (x, y))
        else:
            x = 20
            y = screen.get_height() - 45
            screen.blit(self.lives_sprite, (x, y))
            lives_text = self.font.render(f"x{lives}", True, WHITE)
            screen.blit(lives_text, (x + 45, y + 5))

    def draw_level(self, screen: pygame.Surface, level: int) -> None:
        """Draw the level number at the bottom right."""
        level_label = self.font_small.render(f"LEVEL {level}", True, WHITE)
        level_label_rect = level_label.get_rect()
        level_label_rect.center = (self.screen_width - 95,
                                   self.screen_height - 32)
        screen.blit(level_label, level_label_rect)

    def draw_time(
        self, screen: pygame.Surface, elapsed_seconds: int,
        level_time: int = 90,
    ) -> None:
        """Draw the seconds left in the level at the bottom center.

        Args:
            screen: Surface to draw on.
            elapsed_seconds: Seconds already spent in the level.
            level_time: Time limit of the level in seconds.
        """
        # Never show a negative time.
        time_left = max(0, level_time - elapsed_seconds)
        time_label = self.font_small.render(f"TIME {time_left}", True, WHITE)
        time_label_rect = time_label.get_rect()
        time_label_rect.center = (self.screen_width // 2,
                                  self.screen_height - 30)
        screen.blit(time_label, time_label_rect)

    def draw_cheats(
        self, screen: pygame.Surface, ghosts_frozen: bool
    ) -> None:
        """Show "CHEAT" (and "FROZEN" if ghosts are frozen) at the top left."""
        cheat_label = self.font_small.render("CHEAT", True, YELLOW)
        screen.blit(cheat_label, (20, 20))
        if ghosts_frozen:
            frozen_label = self.font_small.render("FROZEN", True, CYAN)
            screen.blit(frozen_label, (20, 50))
