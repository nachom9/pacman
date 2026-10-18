import pygame

from src.paths import FONT_PATH

RED = (255, 0, 0)
WHITE = (255, 255, 255)

class DeathEndGame:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(FONT_PATH, 50)
        self.font_small = pygame.font.Font(FONT_PATH, 25)
        self.timer = 0

    def blink(self):
        if (self.timer // 1000) % 2 == 1:
            return True
        return False

    def draw(self, screen):
        center_x = self.screen_width // 2

        screen.fill((0, 0, 0))
        death_text = self.font.render("GAME OVER", False, RED)
        death_rect = death_text.get_rect(center=(center_x, self.screen_height // 2 - 60))
        screen.blit(death_text, death_rect)

        if self.blink():
            death_instructions = self.font_small.render("Press Space to Continue", False, WHITE)
            death_instructions_rect = death_instructions.get_rect(center=(center_x, self.screen_height // 2 + 20))
            screen.blit(death_instructions, death_instructions_rect)

    def run(self, screen, clock):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return "continue"

            self.draw(screen)
            pygame.display.flip()
            self.timer += clock.tick(60)
