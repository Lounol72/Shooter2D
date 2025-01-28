import pygame

class PauseMenu:
    def __init__(self, surface, assets):
        self.surface = surface
        self.assets = assets
        # Create a transparent surface
        self.transparent_surface = pygame.Surface((self.surface.get_width(), self.surface.get_height()), pygame.SRCALPHA)
        # Fill it with a transparent color
        self.transparent_surface.fill((0, 0, 0, 0)) 

        # Define the rectangle dimensions and margin
        margin = 50
        rect_width = self.surface.get_width() - 2 * margin
        rect_height = self.surface.get_height() - 2 * margin
        rect_x = margin
        rect_y = margin
        rect_color = (255, 255, 255, 128)  # 50% transparency

        # Draw the semi-transparent background
        pygame.draw.rect(self.surface, (0, 0, 0, 100), [0, 0, self.surface.get_width(), self.surface.get_height()])
        # Blit the transparent surface onto the main surface
        pygame.draw.rect(self.transparent_surface, rect_color, (rect_x, rect_y, rect_width, rect_height), border_radius=20)

    def render(self):
        
        self.surface.blit(self.assets["background_game"], (0, 0))
        self.surface.blit(self.transparent_surface, (0, 0))

        # Calculate the position to center the play button on the X axis
        play_button_x = (self.surface.get_width() - self.assets["play_button"].get_width()) // 2
        play_button_y = self.assets["play_button_rect"].y  # Keep the original Y position

        # Update the play button rect position
        self.assets["play_button_rect"].x = play_button_x
        self.assets["play_button_rect"].y = play_button_y

        # Blit the play button image
        self.surface.blit(self.assets["play_button"], self.assets["play_button_rect"])

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.assets["play_button_rect"].collidepoint(mouse_pos):
                return "resume"
        return None