import pygame


# Classe qui s'occupe des animations

class AnimateSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_name: str, speed=1):
        super().__init__()
        self.image = pygame.image.load(f"assets/{sprite_name}.png")
        self.current_image = 0
        self.images = animation.get(sprite_name)
        self.speed = speed

    # Méthode pour animer le sprite
    def animate(self):
        self.current_image += self.speed
        if self.current_image >= len(self.images):
            self.current_image = 0
        self.image = self.images[int(self.current_image)]

    def update(self, sprite_name, speed):
        self.speed = speed
        self.images = animation.get(sprite_name)


# Fonction pour charger les images d'un sprite

def load_animation_images(dos_name: str, sprite_name: str, number_img: int):
    images = list()
    path = f'assets/{dos_name}/{sprite_name}'

    for num in range(1, number_img):
        image_path = f'{path}{num}.png'
        images.append(pygame.image.load(image_path))
    return images


# Définir un dictionnaire qui va contenir les images chargées de chaque sprite
animation = {
    'Walk_to_left_Zombie_1': load_animation_images('Zombie/Zombie Man/Walk_to_left', 'Zombie', 8),
    'Walk_to_right_Zombie_1': load_animation_images('Zombie/Zombie Man/Walk_to_right', 'Zombie', 8),
    'Attack_Zombie_1': load_animation_images('Zombie/Zombie Man/Attack', 'Attack_', 4),
    'Soldier': load_animation_images('Personnages/Soldier_1/idle', 'Soldier', 7),
    'Walk_to_right_Soldier_1': load_animation_images('Personnages/Soldier_1/Walk_to_right', 'Walk', 7),
    'Shoot_Soldier_1': load_animation_images('Personnages/Soldier_1/Shoot', 'Shoot2_', 4),
    'Reloding_Soldier_1': load_animation_images('Personnages/Soldier_1/Reload', 'Reload', 13)
}
