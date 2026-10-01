import pygame

from src.instructions_menu import InstructionsMenu

FONT_PATH = "assets/fonts/PressStart2P-Regular.ttf"
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

FAKE_SCORES = [
    ("Sannaka", 1110),
    ("foliole", 20),
    ("Marmelade", 20),
    ("goldfish", 20),
]


class MainMenu:

    def __init__(self, screen_width: int, screen_height: int) -> None:
        self.screen_width = screen_width
        self.screen_height = screen_height
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
        rendered = font.render(text, False, color)
        center_x = self.screen_width // 2
        screen.blit(rendered, rendered.get_rect(center=(center_x, y)))

    def draw(self, screen: pygame.Surface) -> None:
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
        y = 450
        for i, (name, score) in enumerate(FAKE_SCORES):
            line = f"{i + 1}. {name}  {score}"
            self._draw_centered(screen, line, self.font, WHITE, y)
            y += 35

    def run(self, screen: pygame.Surface, clock: pygame.time.Clock) -> str:
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
