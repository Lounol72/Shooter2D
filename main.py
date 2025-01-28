import pygame
import gc
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

# Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("assets/audio/Ulysse.mp3")
Font = pygame.font.SysFont("Saira ExtraCondensed Black", 36)

# Screen settings
running = True
surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF, 32)
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
    "game_over_button": pygame.image.load('assets/Game_over.png')
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

def handle_main_menu(event, main_menu, game):
    """Handle events in the main menu."""
    action = main_menu.handle_event(event)
    if action == "play":
        game.is_playing = True
    elif action == "difficulty":
        game.set_difficulty = True
    elif action == "settings":
        game.settings = True

def handle_game_play(game, surface, assets, PauseMenu):
    """Handle game play events and rendering."""
    if game.is_paused:
        PauseMenu.render()
    else:
        game.handle_input()
        surface.blit(assets["background_game"], (0, 0))
        game.update(surface)
        surface.blit(assets["font"].render(f"{game.player.score}", 1, RED), (90, 50))
        surface.blit(assets["font"].render(f"{game.player.magazine}", 1, RED), (90, 70))

def handle_game_over(game_over_menu):
    """Handle game over events and rendering."""
    game_over_menu.render()

def handle_difficulty_menu(event, difficulty_menu, game):
    """Handle events in the difficulty menu."""
    difficulty_menu.render()
    if difficulty_menu.handle_event(event):
        game.set_difficulty = False

def handle_settings_menu(event, settings_menu, game):
    """Handle events in the settings menu."""
    settings_menu.render()
    if settings_menu.handle_event(event) == "back":
        game.settings = False

def process_events(game, main_menu, game_over_menu, pause_menu, difficulty_menu, settings_menu):
    """Process all events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True
            if event.key == pygame.K_ESCAPE and game.is_playing and not game.Game_over:
                game.is_paused = not game.is_paused
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game.is_playing and not game.Game_over:
                handle_main_menu(event, main_menu, game)
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
                handle_difficulty_menu(event, difficulty_menu, game)
            elif game.settings:
                handle_settings_menu(event, settings_menu, game)
    return True

def main_loop():
    """Main game loop."""
    pygame.mixer.music.play(-1)
    global running
    game = Game()
    clock = pygame.time.Clock()
    game.read_fic()
    game.read_max_score()
    main_menu = MainMenu(surface, assets, game.max_score)
    game_over_menu = GameOverMenu(surface, assets, game)
    pause_menu = PauseMenu(surface, assets)
    difficulty_menu = DifficultyMenu(surface, assets, game)
    settings_menu = SettingsMenu(surface, assets)

    while running:
        running = process_events(game, main_menu, game_over_menu, pause_menu, difficulty_menu, settings_menu)

        if game.is_playing and not game.Game_over:
            handle_game_play(game, surface, assets,pause_menu)
        elif game.Game_over:
            handle_game_over(game_over_menu)
        elif game.set_difficulty:
            handle_difficulty_menu(None, difficulty_menu, game)
        elif game.settings:
            handle_settings_menu(None, settings_menu, game)
        else:
            main_menu.render()

        pygame.display.update()
        clock.tick(30)
        
        # Libérer de l'espace dans la RAM
        gc.collect()

    pygame.quit()

if __name__ == "__main__":
    main_loop()