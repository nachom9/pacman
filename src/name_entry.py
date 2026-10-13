import pygame
from src.scores import load_scores, save_score

FONT_PATH = "assets/fonts/PressStart2P-Regular.ttf"
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

class NameEntry:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(FONT_PATH, 35)
        self.font_small = pygame.font.Font(FONT_PATH, 25)
        self.timer = 0
        self.name_text = ''

    def draw(self, screen, score):
        center_x = self.screen_width // 2

        screen.fill((0, 0, 0))
        death_text = self.font.render("Enter your name:", False, WHITE)
        death_rect = death_text.get_rect(center=(center_x, self.screen_height // 2 - 120))
        screen.blit(death_text, death_rect)

        death_instructions = self.font_small.render(f"Your score: {score}", False, WHITE)
        death_instructions_rect = death_instructions.get_rect(center=(center_x, self.screen_height // 2 + 60))
        screen.blit(death_instructions, death_instructions_rect)

        name_text = self.font.render(self.name_text, False, YELLOW)
        name_text_rect = name_text.get_rect(center=(center_x, self.screen_height // 2 - 40))
        screen.blit(name_text, name_text_rect)


    def run(self, screen, clock, score, scores_file_name):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if ((event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN)and
                        len(self.name_text) > 0):
                        save_score(self.name_text, score, scores_file_name)
                        return "score saved"
                    elif event.key == pygame.K_BACKSPACE:
                        self.name_text = self.name_text[:-1]
                    else:
                        if (event.unicode.isalnum() or event.unicode == " " and
                            len(self.name_text) < 10):
                            self.name_text += event.unicode

            self.draw(screen, score)
            pygame.display.flip()
            self.timer += clock.tick(60)
