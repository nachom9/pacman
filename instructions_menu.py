import pygame

FONT_PATH = "assets/fonts/PressStart2P-Regular.ttf"
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

LINES = [
    "ARROWS  Move",
    "ESC     Pause",
    "P       Resume",
    "",
    "Eat all the dots",
    "to win the level.",
    "",
    "Avoid the ghosts!",
    "Big dots let you",
    "eat them for a while.",
]


class InstructionsMenu:
    """Screen that shows the game controls and rules."""

    def __init__(self, screen_width: int, screen_height: int) -> None:
        """Load the fonts once and store the screen size.

        Args:
            screen_width: Width of the game window in pixels.
            screen_height: Height of the game window in pixels.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(FONT_PATH, 50)
        self.font_small = pygame.font.Font(FONT_PATH, 20)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the instructions on the given surface.

        Args:
            screen: Surface to draw on.
        """
        screen.fill((0, 0, 0))
        center_x = self.screen_width // 2

        title = self.font.render("INSTRUCTIONS", False, YELLOW)
        screen.blit(
            title,
            title.get_rect(center=(center_x, self.screen_height // 6)),
        )

        y = self.screen_height // 3
        for line in LINES:
            text = self.font_small.render(line, False, WHITE)
            screen.blit(text, text.get_rect(center=(center_x, y)))
            y += 40

        back = self.font_small.render("Press ESC to go back", False, YELLOW)
        screen.blit(
            back,
            back.get_rect(center=(center_x, self.screen_height - 80)),
        )

    def run(self, screen: pygame.Surface, clock: pygame.time.Clock) -> str:
        """Show the instructions until the player goes back.

        Args:
            screen: Surface to draw on.
            clock: Clock used to limit the frame rate.

        Returns:
            "back" if the player pressed ESC, "quit" if they closed
            the window.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "back"

            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)
