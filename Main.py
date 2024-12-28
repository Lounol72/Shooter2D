import time
from os import getcwd, chdir, mkdir
import pygame
from Game import Game

pygame.init()

# colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (110, 110, 110)
RED = (255, 0, 0)
ORANGE = (249, 92, 14)

Font = pygame.font.SysFont("Saira ExtraCondensed Black", 36)
Score = Font.render

# screen settings

weight = 1080
height = 720
running = True
surface = pygame.display.set_mode((weight, height))
pygame.display.set_caption("Zombie Apocalypse")
pygame.display.set_icon(pygame.image.load("assets/Icon.png"))

# background and defaults images settings and loading

background_game = pygame.transform.scale(pygame.image.load("assets/PNG/War1/Bright/War.png"),
                                         (weight, height))

background_menu = pygame.transform.scale(pygame.image.load("assets/Background_menu_2.jpg"),
                                         (weight, height))
Title_image = pygame.image.load('assets/Title.png')
Title_width = Title_image.get_width()
Title_height = Title_image.get_height()

Play_button = pygame.transform.scale(pygame.image.load('assets/Fonts/Buttons/Playbutton.png'), (75, 49))
Play_button_rect = Play_button.get_rect()
Play_button_rect.x = 50
Play_button_rect.y = height - 120

Difficulty_button = pygame.transform.scale(pygame.image.load('assets/Fonts/Buttons/Difficultybutton.png'), (119, 56))
Difficulty_button_rect = Difficulty_button.get_rect()
Difficulty_button_rect.x = 50
Difficulty_button_rect.y = height - 195

Game_over_button = pygame.image.load('assets/Game_over.Png')
Game_over_button_rect = Game_over_button.get_rect()
Game_over_button_rect.x = (1080 - 360) // 2
Game_over_button_rect.y = (720 - 360) // 2

game = Game()
clock = pygame.time.Clock()

# Main loop
game.read_fic()
while running:

    # Handeling events ( in rows)

    if game.is_playing and not game.Game_over:

        # Lauching game if we click

        game.handle_input()
        surface.blit(background_game, (0, 0))
        game.update(surface)
        surface.blit(Font.render(f"{game.player.score}", 1, (255, 0, 0)),
                     (90, 50))
        surface.blit(Font.render(f"{game.player.magazine}", 1, (255, 0, 0)),
                     (90, 70))

    elif game.Game_over:

        game.all_monsters = pygame.sprite.Group()
        game.player.health = game.player.max_health
        if len(game.player_high_score) == 0 or game.player.score > max(game.player_high_score):
            game.player_high_score.append(game.player.score)
            surface.blit(Font.render(f"Nouveau Meilleur score!", 1, (255, 0, 0)),
                         (1080 // 2 - 90, 720 - 100))

        surface.blit(pygame.transform.scale(pygame.image.load("assets/Background_menu_2.jpg"),
                                            (1080, 720)), (0, 0))

        pygame.draw.rect(surface, GREY, [Game_over_button_rect.x, Game_over_button_rect.y,Game_over_button.get_width(), Game_over_button.get_height()])
        surface.blit(Font.render(f"Votre score est de :  {game.player_high_score[-1]} !", 1, (255, 0, 0)),
                     (1080 // 2 - 90, 720 - 50))

        surface.blit(Game_over_button, (Game_over_button_rect.x, Game_over_button_rect.y))


    else:

        # Staying on the menu
        surface.blit(background_menu, (0, 0))
        surface.blit(Title_image, ((weight - Title_width) // 2, 120))
        pygame.draw.rect(surface, GREY,
                         [Play_button_rect.x - 15, Play_button_rect.y - 9, Play_button.get_width() + 20,
                          Play_button.get_height() + 18])
        pygame.draw.rect(surface, GREY,
                         [Play_button_rect.x - 15, Play_button_rect.y - 9, Play_button.get_width() + 20,
                          Play_button.get_height() + 18])
        pygame.draw.rect(surface, GREY,
                         [Difficulty_button_rect.x - 15, Difficulty_button_rect.y - 9, Difficulty_button.get_width() + 20,
                          Difficulty_button.get_height() + 18])
        pygame.draw.rect(surface, GREY,
                         [Difficulty_button_rect.x - 15, Difficulty_button_rect.y - 9, Difficulty_button.get_width() + 20,
                          Difficulty_button.get_height() + 18])

        if Play_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(surface, ORANGE,
                             [Play_button_rect.x - 14, Play_button_rect.y - 8, Play_button.get_width() + 18,
                              Play_button.get_height() + 17])

        if Difficulty_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(surface, ORANGE,
                             [Difficulty_button_rect.x - 14, Difficulty_button_rect.y - 8, Difficulty_button.get_width() + 18,
                              Difficulty_button.get_height() + 17])

        surface.blit(Difficulty_button,(Difficulty_button_rect.x, Difficulty_button_rect.y))
        surface.blit(Play_button, (Play_button_rect.x, Play_button_rect.y))
        if len(game.player_high_score) != 0:
            surface.blit(Font.render(f"Votre score maximal est de :  {max(game.player_high_score)} !", 1, (255, 0, 0)),
                         (1080 // 2 - 90, 720 - 50))
        else:
            surface.blit(Font.render(f"Lancez votre première partie !", 1, (255, 0, 0)),
                         (1080 // 2 - 180, 720 - 50))

    # Handleing events ( click per click)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_END:
                if game.is_playing:
                    game.is_playing = not game.is_playing
                else:
                    game.start()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if Play_button_rect.collidepoint(event.pos):
                game.start()
            if Game_over_button_rect.collidepoint(event.pos) and game.Game_over:
                game.Game_over = not game.is_playing
                game.is_playing = not game.is_playing
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    # les Fps sont set à 30/s
    clock.tick(30)

pygame.quit()
quit()
