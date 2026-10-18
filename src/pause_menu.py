import pygame

from src.paths import FONT_PATH

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)


class PauseMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(FONT_PATH, 50)
        self.font_small = pygame.font.Font(FONT_PATH, 25)

    def draw(self, screen):
        center_x = self.screen_width // 2

        pause_text = self.font.render("PAUSED", False, WHITE)
        pause_rect = pause_text.get_rect(center=(center_x, self.screen_height // 4))
        pygame.draw.rect(screen, BLACK, pause_rect.inflate(30, 20))
        screen.blit(pause_text, pause_rect)

        pause_instructions = self.font_small.render("Press P or ESC to Resume", False, WHITE)
        instructions_rect = pause_instructions.get_rect(center=(center_x, self.screen_height // 2))
        pygame.draw.rect(screen, BLACK, instructions_rect.inflate(30, 20))
        screen.blit(pause_instructions, instructions_rect)

        menu_instructions = self.font_small.render(
            "Press M for Main Menu", False, WHITE
        )
        menu_rect = menu_instructions.get_rect(
            center=(center_x, self.screen_height // 2 + 50)
        )
        pygame.draw.rect(screen, BLACK, menu_rect.inflate(30, 20))
        screen.blit(menu_instructions, menu_rect)

    def run(self, screen: pygame.Surface, clock: pygame.time.Clock) -> str:
        """Wait until the player resumes, goes to the menu or quits.

        Returns:
            "resume" (P or ESC), "menu" (M) or "quit" (window closed).
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_p, pygame.K_ESCAPE):
                        return "resume"
                    if event.key == pygame.K_m:
                        return "menu"

            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)
