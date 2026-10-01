import pygame


class HUD:
    def __init__(self, screen_width, screen_height, spritesheet):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(
            "assets/fonts/PressStart2P-Regular.ttf",
            25
        )
        self.font_small = pygame.font.Font(
            "assets/fonts/PressStart2P-Regular.ttf",
            18
        )
        self.lives_sprite = spritesheet.subsurface(pygame.Rect(595, 601, 24, 26))

    def draw_score(self, screen, score):
        score_label = self.font.render("SCORE", True, (255, 255, 255))
        score_value = self.font.render(str(score), True, (255, 255, 255))
        
        score_label_rect = score_label.get_rect()
        score_value_rect = score_value.get_rect()
        
        score_label_rect.center = (screen.get_width() // 2, 30)
        score_value_rect.center = (screen.get_width() // 2, 65)
        
        screen.blit(score_label, score_label_rect)
        screen.blit(score_value, score_value_rect)

    def draw_lives(self, screen, lives):
        if lives <= 5:
            for i in range(lives):
                x = 20 + i * 40
                y = screen.get_height() - 45

                screen.blit(
                    self.lives_sprite,
                    (x, y)
                )

        else:
            x = 20
            y = screen.get_height() - 45

            screen.blit(
                self.lives_sprite,
                (x, y)
            )

            lives_text = self.font.render(
                f"x{lives}",
                True,
                (255, 255, 255)
            )

            screen.blit(
                lives_text,
                (x + 45, y + 5)
            )

    def draw_level(self, screen, level):
        level_label = self.font_small.render(f"LEVEL {level}", True, (255, 255, 255))
        level_label_rect = level_label.get_rect()
        level_label_rect.center = (self.screen_width - 95, self.screen_height - 32)    
        screen.blit(level_label, level_label_rect)

    def draw_time(self, screen, elapsed_seconds, level_time=90):
        time_left = level_time - elapsed_seconds

        if time_left < 0:
            time_left = 0

        time_label = self.font_small.render(f"TIME {time_left}", True, (255, 255, 255))
        time_label_rect = time_label.get_rect()
        time_label_rect.center = (self.screen_width // 2, self.screen_height - 30)
        screen.blit(time_label, time_label_rect)
