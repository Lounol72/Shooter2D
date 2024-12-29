import pygame
from Game import Game
from menus.main_menu import MainMenu
from menus.game_over_menu import GameOverMenu

# Constants
WIDTH = 1080
HEIGHT = 720
RED = (255, 0, 0)
GREY = (110, 110, 110)

# Initialize Pygame
pygame.init()
Font = pygame.font.SysFont("Saira ExtraCondensed Black", 36)
Score = Font.render

# Screen settings
running = True
surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Apocalypse")
pygame.display.set_icon(pygame.image.load("assets/Icon.png"))

# Load assets
assets = {
    "background_game": pygame.transform.scale(pygame.image.load("assets/PNG/War1/Bright/War.png"), (WIDTH, HEIGHT)),
    "background_menu": pygame.transform.scale(pygame.image.load("assets/Background_menu_2.jpg"), (WIDTH, HEIGHT)),
    "title_image": pygame.image.load('assets/Title.png'),
    "play_button": pygame.transform.scale(pygame.image.load('assets/Fonts/Buttons/Playbutton.png'), (75, 49)),
    "difficulty_button": pygame.transform.scale(pygame.image.load('assets/Fonts/Buttons/Difficultybutton.png'), (119, 56)),
    "game_over_button": pygame.image.load('assets/Game_over.Png')
}

# Get dimensions for title image
assets["title_width"] = assets["title_image"].get_width()
assets["title_height"] = assets["title_image"].get_height()

# Get rects for buttons
button_positions = {
    "play_button_rect": (50, HEIGHT - 120),
    "difficulty_button_rect": (50, HEIGHT - 195),
    "game_over_button_rect": ((WIDTH - 360) // 2, (HEIGHT - 360) // 2)
}

for key, pos in button_positions.items():
    rect = assets[key.replace('_rect', '')].get_rect()
    rect.x, rect.y = pos
    assets[key] = rect

def main_loop():
    global running
    game = Game()
    clock = pygame.time.Clock()
    game.read_fic()

    main_menu = MainMenu(surface, assets)
    game_over_menu = GameOverMenu(surface, assets, game)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                game.pressed[event.key] = True
            elif event.type == pygame.KEYUP:
                game.pressed[event.key] = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game.is_playing and not game.Game_over:
                    action = main_menu.handle_event(event)
                    actions = {
                        "play": lambda: setattr(game, 'is_playing', True),
                        "difficulty": lambda: None  # Handle difficulty change
                    }
                    actions.get(action, lambda: None)()
                elif game.Game_over:
                    action = game_over_menu.handle_event(event)
                    if action == "restart":
                        game.Game_over = False
                        game.is_playing = True

        if game.is_playing and not game.Game_over:
            game.handle_input()
            surface.blit(assets["background_game"], (0, 0))
            game.update(surface)
            surface.blit(Font.render(f"{game.player.score}", 1, RED), (90, 50))
            surface.blit(Font.render(f"{game.player.magazine}", 1, RED), (90, 70))

        elif game.Game_over:
            game_over_menu.render()

        else:
            main_menu.render()

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main_loop()
