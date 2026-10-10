import pygame

FONT_PATH = "assets/fonts/PressStart2P-Regular.ttf"
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
        print(self.timer // 1000, (self.timer // 1000) % 2)
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

    def run(self, screen, clock, score):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

            self.draw(screen)
            pygame.display.flip()
            self.timer += clock.tick(60)


'''
    def draw(self, screen):
        center_x = self.screen_width // 2

        pause_text = self.font.render("PAUSED", False, WHITE)
        pause_rect = pause_text.get_rect(center=(center_x, self.screen_height // 4))
        screen.blit(pause_text, pause_rect)

        pause_instructions = self.font_small.render("Press P to Resume", False, WHITE)
        instructions_rect = pause_instructions.get_rect(center=(center_x, self.screen_height // 2))
        screen.blit(pause_instructions, instructions_rect)
'''
