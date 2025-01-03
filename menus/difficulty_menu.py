import pygame

class DifficultyMenu:
    def __init__(self, surface, assets, game):
        self.surface = surface
        self.assets = assets
        self.game = game
        self.buttons = {
            "easy": pygame.Rect(0, 0, 200, 50),
            "medium": pygame.Rect(0, 0, 200, 50),
            "hard": pygame.Rect(0, 0, 200, 50),
            "extreme": pygame.Rect(0, 0, 200, 50)
        }
        
    def render(self):
        # Create a transparent surface
        transparent_surface = pygame.Surface((self.surface.get_width(), self.surface.get_height()), pygame.SRCALPHA)
        # Fill it with a transparent color
        transparent_surface.fill((0, 0, 0, 0)) 
        
        # Define the rectangle dimensions and margin
        margin = 50
        rect_width = self.surface.get_width() - 2 * margin
        rect_height = self.surface.get_height() - 2 * margin
        rect_x = margin
        rect_y = margin
        rect_color = (255, 255, 255, 128)  # 50% transparency

        pygame.draw.rect(self.surface, (0, 0, 0, 100), [0, 0, self.surface.get_width(), self.surface.get_height()])
        self.surface.blit(self.assets["background_game"], (0, 0))
        # Blit the transparent surface onto the main surface
        pygame.draw.rect(transparent_surface, rect_color, (rect_x, rect_y, rect_width, rect_height), border_radius=20)
        self.surface.blit(transparent_surface, (0, 0))

        # Calculate the position to center the buttons
        button_margin = 20
        button_width = 200
        button_height = 50
        start_y = (self.surface.get_height() - (button_height * 4 + button_margin * 3)) // 2

        for i, (difficulty, rect) in enumerate(self.buttons.items()):
            rect.x = (self.surface.get_width() - button_width) // 2
            rect.y = start_y + i * (button_height + button_margin)
            pygame.draw.rect(self.surface, (110, 110, 110), rect)
            text_surface = self.assets["font"].render(difficulty.capitalize(), True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=rect.center)
            self.surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for difficulty, rect in self.buttons.items():
                if rect.collidepoint(mouse_pos):
                    self.game.set_difficulty = False  # Set set_difficulty to False
                    self.game.difficulty = difficulty  # Update the game's difficulty
                    return difficulty
        return None