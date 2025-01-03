import pygame

class SettingsMenu:
    def __init__(self, surface, assets):
        self.surface = surface
        self.assets = assets
        self.volume = pygame.mixer.music.get_volume()
        self.buttons = {
            "volume_up": pygame.Rect(0, 0, 200, 50),
            "volume_down": pygame.Rect(0, 0, 200, 50),
            "back": pygame.Rect(0, 0, 200, 50)
        }

    def render(self):
        self.surface.blit(self.assets["background_menu"], (0, 0))

        button_margin = 20
        button_width = 200
        button_height = 50
        start_y = self.surface.get_height() - (button_height + button_margin) * len(self.buttons) - 20

        for i, (label, rect) in enumerate(self.buttons.items()):
            rect.x = 20
            rect.y = start_y + i * (button_height + button_margin)
            pygame.draw.rect(self.surface, (110, 110, 110), rect)
            text_surface = self.assets["font"].render(label.replace('_', ' ').capitalize(), True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=rect.center)
            self.surface.blit(text_surface, text_rect)

        volume_surface = self.assets["font"].render(f"Volume: {int(self.volume * 100)}%", True, (255, 255, 255))
        volume_rect = volume_surface.get_rect(center=(self.surface.get_width() // 2, 100))
        self.surface.blit(volume_surface, volume_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for label, rect in self.buttons.items():
                if rect.collidepoint(mouse_pos):
                    if label == "volume_up":
                        self.volume = min(1.0, self.volume + 0.1)
                        pygame.mixer.music.set_volume(self.volume)
                    elif label == "volume_down":
                        self.volume = max(0.0, self.volume - 0.1)
                        pygame.mixer.music.set_volume(self.volume)
                    elif label == "back":
                        return "back"
        return None