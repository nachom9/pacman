"""Main menu: start, instructions, quit and the top 10 highscores."""

from typing import Any

import pygame

from src.instructions_menu import InstructionsMenu
from src.paths import FONT_PATH
from src.scores import load_scores

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)


class MainMenu:
    """First screen of the game."""

    def __init__(
        self, screen_width: int, screen_height: int, scores_file_name: str
    ) -> None:
        """Load the fonts and create the instructions screen.

        Args:
            screen_width: Width of the window in pixels.
            screen_height: Height of the window in pixels.
            scores_file_name: Path of the highscores JSON file.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scores_file_name = scores_file_name
        self.scores: list[dict[str, Any]] = []
        self.title_font = pygame.font.Font(FONT_PATH, 60)
        self.font = pygame.font.Font(FONT_PATH, 20)
        self.instructions = InstructionsMenu(screen_width, screen_height)

    def _draw_centered(
        self,
        screen: pygame.Surface,
        text: str,
        font: pygame.font.Font,
        color: tuple[int, int, int],
        y: int,
    ) -> None:
        """Draw a text centered horizontally at height y."""
        rendered = font.render(text, False, color)
        center_x = self.screen_width // 2
        screen.blit(rendered, rendered.get_rect(center=(center_x, y)))

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the title, the controls and the highscores."""
        screen.fill((0, 0, 0))

        self._draw_centered(screen, "PACMAN", self.title_font, YELLOW, 120)

        self._draw_centered(
            screen, "Press SPACE to Start", self.font, WHITE, 230
        )
        self._draw_centered(
            screen, "Press Q for Instructions", self.font, WHITE, 270
        )
        self._draw_centered(
            screen, "Press ESC to Quit", self.font, WHITE, 310
        )

        self._draw_centered(screen, "HIGHSCORES", self.font, YELLOW, 400)
        if not self.scores:
            self._draw_centered(screen, "No scores yet", self.font, WHITE, 450)
        y = 450
        for i, entry in enumerate(self.scores):
            line = f"{i + 1}. {entry['name']}  {entry['score']}"
            self._draw_centered(screen, line, self.font, WHITE, y)
            y += 35

    def run(self, screen: pygame.Surface, clock: pygame.time.Clock) -> str:
        """Show the menu until the player starts a game or quits.

        Returns:
            "play" (Space) or "quit" (ESC or window closed).
        """
        # Read the file once each time the menu opens (not on every frame),
        # so a score saved at the end of a game shows up straight away.
        self.scores = load_scores(self.scores_file_name)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return "play"
                    if event.key == pygame.K_q:
                        if self.instructions.run(screen, clock) == "quit":
                            return "quit"
                    if event.key == pygame.K_ESCAPE:
                        return "quit"

            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)
