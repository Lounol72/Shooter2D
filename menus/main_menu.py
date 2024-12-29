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

    def render(self):
        self.surface.blit(self.assets["background_menu"], (0, 0))
        self.surface.blit(self.assets["title_image"], ((self.surface.get_width() - self.assets["title_width"]) // 2, 120))
        pygame.draw.rect(self.surface, (110, 110, 110), [self.assets["play_button_rect"].x - 15, self.assets["play_button_rect"].y - 9, self.assets["play_button"].get_width() + 20, self.assets["play_button"].get_height() + 18])
        pygame.draw.rect(self.surface, (110, 110, 110), [self.assets["difficulty_button_rect"].x - 15, self.assets["difficulty_button_rect"].y - 9, self.assets["difficulty_button"].get_width() + 20, self.assets["difficulty_button"].get_height() + 18])
        self.surface.blit(self.assets["play_button"], self.assets["play_button_rect"])
        self.surface.blit(self.assets["difficulty_button"], self.assets["difficulty_button_rect"])
        self.surface.blit(pygame.font.SysFont("Saira ExtraCondensed Black", 36).render(f"Max Score: {self.max_score}", 1, (255, 0, 0)), (50, 50))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.assets["play_button_rect"].collidepoint(mouse_pos):
                return "play"
            elif self.assets["difficulty_button_rect"].collidepoint(mouse_pos):
                return "difficulty"
        return None