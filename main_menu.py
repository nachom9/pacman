import pygame
from instructions_menu import InstructionsMenu

FONT_PATH = "assets/fonts/PressStart2P-Regular.ttf"
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)


class MainMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title_font = pygame.font.Font(FONT_PATH, 60)
        self.font = pygame.font.Font(FONT_PATH, 20)
        self.instructions = InstructionsMenu(screen_width, screen_height)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        center_x = self.screen_width // 2
 
        title = self.title_font.render("PACMAN", False, YELLOW)
        screen.blit(
            title,
            title.get_rect(center=(center_x, self.screen_height // 4)),
        )
 
        start = self.font.render("Press SPACE to Start", False, WHITE)
        screen.blit(
            start,
            start.get_rect(center=(center_x, self.screen_height // 2)),
        )
 
        quit_text = self.font.render("Press ESC to Quit", False, WHITE)
        screen.blit(
            quit_text,
            quit_text.get_rect(
                center=(center_x, self.screen_height // 2 + 100)
            ),
        )

        instructions_text = self.font.render("Press Q to Instructions", False, WHITE)
        screen.blit(
            instructions_text,
            instructions_text.get_rect(
                center=(center_x, self.screen_height // 2 + 50)
            ),
        )

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
