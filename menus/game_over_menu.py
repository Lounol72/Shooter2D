import pygame

class GameOverMenu:
    def __init__(self, surface, assets, game):
        self.surface = surface
        self.assets = assets
        self.game = game
        self.buttons = {
            "restart": pygame.Rect(0, 0, 200, 50),
            "menu": pygame.Rect(0, 0, 200, 50)
        }

    def render(self):
        self.surface.blit(self.assets["background_menu"], (0, 0))
        
        # Draw the game over text
        game_over_surface = self.assets["title_font"].render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_surface.get_rect(center=(self.surface.get_width() // 2, 100))
        self.surface.blit(game_over_surface, game_over_rect)
        
        button_margin = 20
        button_width = 200
        button_height = 50
        start_y = game_over_rect.bottom + 50

        for i, (label, rect) in enumerate(self.buttons.items()):
            rect.x = (self.surface.get_width() - button_width) // 2
            rect.y = start_y + i * (button_height + button_margin)
            pygame.draw.rect(self.surface, (110, 110, 110), rect)
            text_surface = self.assets["font"].render(label.capitalize(), True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=rect.center)
            self.surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for label, rect in self.buttons.items():
                if rect.collidepoint(mouse_pos):
                    return label
        return None