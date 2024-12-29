import pygame

class GameOverMenu:
    def __init__(self, surface, assets, game):
        self.surface = surface
        self.assets = assets
        self.game = game

    def render(self):
        self.game.all_monsters = pygame.sprite.Group()
        self.game.player.health = self.game.player.max_health
        if len(self.game.player_high_score) == 0 or self.game.player.score > max(self.game.player_high_score):
            self.game.player_high_score.append(self.game.player.score)
            self.surface.blit(pygame.font.SysFont("Saira ExtraCondensed Black", 36).render("Nouveau Meilleur score!", 1, (255, 0, 0)), (self.surface.get_width() // 2 - 90, self.surface.get_height() - 100))

        self.surface.blit(self.assets["background_menu"], (0, 0))
        pygame.draw.rect(self.surface, (110, 110, 110), [self.assets["game_over_button_rect"].x, self.assets["game_over_button_rect"].y, self.assets["game_over_button"].get_width(), self.assets["game_over_button"].get_height()])
        self.surface.blit(pygame.font.SysFont("Saira ExtraCondensed Black", 36).render(f"Votre score est de :  {self.game.player_high_score[-1]} !", 1, (255, 0, 0)), (self.surface.get_width() // 2 - 90, self.surface.get_height() - 50))
        self.surface.blit(self.assets["game_over_button"], (self.assets["game_over_button_rect"].x, self.assets["game_over_button_rect"].y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.assets["game_over_button_rect"].collidepoint(mouse_pos):
                return "restart"
        return None