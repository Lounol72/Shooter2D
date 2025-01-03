import pygame
from Game import Game
from menus.main_menu import MainMenu
from menus.game_over_menu import GameOverMenu
from menus.pause_menu import PauseMenu
from menus.difficulty_menu import DifficultyMenu
from menus.settings_menu import SettingsMenu

# Constants
WIDTH = 1080
HEIGHT = 720
RED = (255, 0, 0)
GREY = (110, 110, 110)

# Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("assets/audio/Ulysse.mp3")
Font = pygame.font.SysFont("Saira ExtraCondensed Black", 36)
Score = Font.render

# Screen settings
running = True
surface = pygame.display.set_mode((WIDTH, HEIGHT),pygame.DOUBLEBUF, 32)
pygame.display.set_caption("Zombie Apocalypse")
pygame.display.set_icon(pygame.image.load("assets/Icon.png"))

# Load assets
assets = {
    "background_game": pygame.transform.scale(pygame.image.load("assets/PNG/War1/Bright/War.png"), (WIDTH, HEIGHT)),
    "background_menu": pygame.transform.scale(pygame.image.load("assets/Background_menu_2.jpg"), (WIDTH, HEIGHT)),
    "font": pygame.font.Font("assets/Fonts/Call of Ops Duty.otf", 24),
    "title_font": pygame.font.Font("assets/Fonts/Call of Ops Duty.otf", 72),
    "title_image": pygame.image.load('assets/Title.png'),
    "play_button": pygame.transform.scale(pygame.image.load('assets/Fonts/Buttons/Playbutton.png'), (75, 49)),
    "difficulty_button": pygame.transform.scale(pygame.image.load('assets/Fonts/Buttons/Difficultybutton.png'), (119, 56)),
    "game_over_button": pygame.image.load('assets/Game_over.Png')
}

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
    pygame.mixer.music.play(-1)
    global running
    game = Game()
    clock = pygame.time.Clock()
    game.read_fic()
    game.read_max_score()
    main_menu = MainMenu(surface, assets,game.max_score)
    game_over_menu = GameOverMenu(surface, assets, game)
    pause_menu = PauseMenu(surface, assets)
    difficulty_menu = DifficultyMenu(surface, assets,game)
    settings_menu = SettingsMenu(surface, assets)

    while running:
        print(game.set_difficulty)
        print(game.Game_over)
        print(game.is_playing)
        print(game.is_paused)
        print(game.max_score)
        print('\n')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                game.pressed[event.key] = True
                if event.key == pygame.K_ESCAPE and game.is_playing and not game.Game_over:
                    game.is_paused = not game.is_paused  # Toggle pause state
            elif event.type == pygame.KEYUP:
                game.pressed[event.key] = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game.is_playing and not game.Game_over:
                    action = main_menu.handle_event(event)
                    actions = {
                        "play": lambda: setattr(game, 'is_playing', True),
                        "difficulty": lambda: setattr(game, 'set_difficulty', True)  # Handle difficulty change
                    }
                    actions.get(action, lambda: None)()
                elif game.Game_over:
                    action = game_over_menu.handle_event(event)
                    if action == "restart":
                        game.Game_over = False
                        game.is_playing = True
                    elif action == "menu":
                        game.Game_over = False
                        game.is_playing = False
                elif game.is_paused:
                    action = pause_menu.handle_event(event)
                    if action == "resume":
                        game.is_paused = False
                elif game.set_difficulty:
                    action = difficulty_menu.handle_event(event)
                    if action:
                        game.set_difficulty = False
                elif game.settings:
                    settings_menu.render()
                    action = settings_menu.handle_event(event)
                    if action == "back":
                        game.settings = False
                

        if game.is_playing and not game.Game_over:
            if game.is_paused:
                pause_menu.render()
            else:
                game.handle_input()
                surface.blit(assets["background_game"], (0, 0))
                game.update(surface)
                surface.blit(assets["font"].render(f"{game.player.score}", 1, (255, 0, 0)), (90, 50))
                surface.blit(assets["font"].render(f"{game.player.magazine}", 1, (255, 0, 0)), (90, 70))
        elif game.Game_over:
            game_over_menu.render()
        elif game.set_difficulty:
            difficulty_menu.render()
            difficulty_menu.handle_event(event)
                
        else:
            main_menu.render()
            main_menu.handle_event(event)
            action = main_menu.handle_event(event)
            if action == "play":
                game.is_playing = True
            elif action == "difficulty":
                game.set_difficulty = True
            elif action == "settings":
                game.settings = True
                

        pygame.display.update()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main_loop()
