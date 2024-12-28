import pygame
from Game import Game

pygame.init()

weight = 1080
height = 720

surface = pygame.display.set_mode((weight,height))
pygame.display.set_caption("Zombie Apocalypse")
#pygame.display.set_icon(pygame.image.load("assets/icone"))
background_game = pygame.transform.scale(pygame.image.load("assets/Cartoon_Forest_Bg_04.png"),(weight,height))
Herbe = pygame.transform.scale(pygame.image.load("assets/Ground.png"),(weight,height))
#background_menu = pygame.transform.scale(pygame.image.load("assets/bg_menu"),(weight,height))

game = Game()

Blue = (0,0,255)
Green = (0,255,0)
Red = (255,0,0)

On = True

while On:

    surface.blit(background_game,(0,0))

    surface.blit(game.player.image,game.player.rect)

    surface.blit(Herbe,(0,0))

    game.player.all_bullets.draw(surface)



    if game.pressed.get(pygame.K_a) and game.player.rect.x >= 0:
        game.player.IsMovingLeft()
    if game.pressed.get(pygame.K_d) and game.player.rect.x < (weight-game.player.weight):
        game.player.IsMovingright()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            On = False

        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

            if event.key == pygame.K_SPACE:
                game.player.shoot()
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False



    pygame.display.update()


pygame.quit()
quit()