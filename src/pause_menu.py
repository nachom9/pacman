import pygame

FONT_PATH = "assets/fonts/PressStart2P-Regular.ttf"
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
        screen.blit(pause_text, pause_rect)

        pause_instructions = self.font_small.render("Press P to Resume", False, WHITE)
        instructions_rect = pause_instructions.get_rect(center=(center_x, self.screen_height // 2))
        screen.blit(pause_instructions, instructions_rect)

    def run(self, screen: pygame.Surface, clock: pygame.time.Clock) -> str:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        return "resume"

            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)
