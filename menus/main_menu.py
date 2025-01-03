import pygame

"""Manages the rendering of the main menu screen in a game.

Handles the visual composition of the main menu, including background, title, and interactive buttons.

Attributes:
    surface (pygame.Surface): The display surface where menu elements are drawn.
    assets (dict): A dictionary containing pre-loaded menu graphics and button configurations.

Methods:
    render: Draws all menu elements onto the game surface, including background, title, and buttons.
"""
class MainMenu:
    def __init__(self, surface, assets, max_score):
        self.surface = surface
        self.assets = assets
        self.max_score = max_score
        self.buttons = {
            "play": pygame.Rect(0, 0, 200, 50),
            "parametre": pygame.Rect(0, 0, 200, 50),
            "difficulty": pygame.Rect(0, 0, 200, 50)
        }

    def render(self):
        self.surface.blit(self.assets["background_menu"], (0, 0))

        # Draw the title
        title_surface = self.assets["title_font"].render("Shooter 2D", True, (0, 0, 0))
        title_rect = title_surface.get_rect(center=(self.surface.get_width() // 2, 100))
        self.surface.blit(title_surface, title_rect)

        button_margin = 20
        button_width = 200
        button_height = 50
        start_y = self.surface.get_height() - (button_height + button_margin) * len(self.buttons) - 20

        for i, (label, rect) in enumerate(self.buttons.items()):
            rect.x = 20
            rect.y = start_y + i * (button_height + button_margin)
            pygame.draw.rect(self.surface, (110, 110, 110), rect)
            text_surface = self.assets["font"].render(label.capitalize(), True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=rect.center)
            self.surface.blit(text_surface, text_rect)

        # Draw the max score if it's different from 0
        if self.max_score != 0:
            score_surface = self.assets["font"].render(f"Best Score: {self.max_score}", True, (0, 0, 0))
            score_rect = score_surface.get_rect(center=(self.surface.get_width() // 2, rect.y + button_height + 30))
            self.surface.blit(score_surface, score_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for label, rect in self.buttons.items():
                if rect.collidepoint(mouse_pos):
                    return label
        return None