"""Screen where the player types a name to save the score."""

import pygame

from src.paths import FONT_PATH
from src.scores import MAX_NAME_LENGTH, save_score

RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)


class NameEntry:
    """Ask for the player name and save the score in the highscores."""

    def __init__(self, screen_width: int, screen_height: int) -> None:
        """Load the fonts used by the screen.

        Args:
            screen_width: Width of the window in pixels.
            screen_height: Height of the window in pixels.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(FONT_PATH, 35)
        self.font_small = pygame.font.Font(FONT_PATH, 25)
        self.timer = 0
        self.name_text = ''

    def draw(self, screen: pygame.Surface, score: int) -> None:
        """Draw the prompt, the name typed so far and the score."""
        center_x = self.screen_width // 2

        screen.fill((0, 0, 0))
        death_text = self.font.render("Enter your name:", False, WHITE)
        death_rect = death_text.get_rect(
            center=(center_x, self.screen_height // 2 - 120)
        )
        screen.blit(death_text, death_rect)

        death_instructions = self.font_small.render(f"Your score: {score}",
                                                    False, WHITE)
        death_instructions_rect = death_instructions.get_rect(
            center=(center_x, self.screen_height // 2 + 60)
        )
        screen.blit(death_instructions, death_instructions_rect)

        name_text = self.font.render(self.name_text, False, YELLOW)
        name_text_rect = name_text.get_rect(
            center=(center_x, self.screen_height // 2 - 40)
        )
        screen.blit(name_text, name_text_rect)

    def run(
        self, screen: pygame.Surface, clock: pygame.time.Clock, score: int,
        scores_file_name: str,
    ) -> str:
        """Let the player type a name, then save the score with Enter.

        Only letters, digits and spaces are accepted, up to 10 characters.

        Args:
            screen: Window surface to draw on.
            clock: Clock used to limit the frame rate.
            score: Final score of the game.
            scores_file_name: Path of the highscores JSON file.

        Returns:
            "score saved" after Enter, "quit" if the window is closed.
        """
        self.name_text = ''
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    enter = event.key in (pygame.K_KP_ENTER,
                                          pygame.K_RETURN)
                    if enter and len(self.name_text) > 0:
                        save_score(self.name_text, score, scores_file_name)
                        return "score saved"
                    elif event.key == pygame.K_BACKSPACE:
                        self.name_text = self.name_text[:-1]
                    else:
                        if ((event.unicode.isalnum() or
                                event.unicode == " ") and
                                len(self.name_text) < MAX_NAME_LENGTH):
                            self.name_text += event.unicode

            self.draw(screen, score)
            pygame.display.flip()
            self.timer += clock.tick(60)
