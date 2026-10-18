"""Game Over screen."""

import pygame

from src.paths import FONT_PATH

RED = (255, 0, 0)
WHITE = (255, 255, 255)


class DeathEndGame:
    """Show "GAME OVER" and the final score when all lives are lost."""

    def __init__(self, screen_width: int, screen_height: int) -> None:
        """Load the fonts used by the screen.

        Args:
            screen_width: Width of the window in pixels.
            screen_height: Height of the window in pixels.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(FONT_PATH, 50)
        self.font_small = pygame.font.Font(FONT_PATH, 25)
        self.timer = 0

    def blink(self) -> bool:
        """Return True on the seconds the instructions must be shown."""
        return (self.timer // 1000) % 2 == 1

    def draw(self, screen: pygame.Surface, score: int) -> None:
        """Draw the title, the final score and the instructions."""
        center_x = self.screen_width // 2

        screen.fill((0, 0, 0))
        death_text = self.font.render("GAME OVER", False, RED)
        death_rect = death_text.get_rect(
            center=(center_x, self.screen_height // 2 - 80)
        )
        screen.blit(death_text, death_rect)

        score_text = self.font_small.render(f"Final score: {score}",
                                            False, WHITE)
        score_rect = score_text.get_rect(
            center=(center_x, self.screen_height // 2)
        )
        screen.blit(score_text, score_rect)

        if self.blink():
            death_instructions = self.font_small.render(
                "Press Space to Continue", False, WHITE
            )
            death_instructions_rect = death_instructions.get_rect(
                center=(center_x, self.screen_height // 2 + 80)
            )
            screen.blit(death_instructions, death_instructions_rect)

    def run(
        self, screen: pygame.Surface, clock: pygame.time.Clock, score: int
    ) -> str:
        """Show the screen until the player presses Space.

        Args:
            screen: Window surface to draw on.
            clock: Clock used to limit the frame rate.
            score: Final score of the game.

        Returns:
            "continue" when Space is pressed, "quit" if the window is closed.
        """
        self.timer = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return "continue"

            self.draw(screen, score)
            pygame.display.flip()
            self.timer += clock.tick(60)
