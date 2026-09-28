import pygame


class HUD:
    def __init__(self, screen_width, spritesheet):
        self.screen_width = screen_width
        self.font = pygame.font.Font(
            "assets/fonts/PressStart2P-Regular.ttf",
            25
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
