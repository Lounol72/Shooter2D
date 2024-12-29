import pygame
import os

# Classe qui s'occupe des animations
class Animate_Sprite(pygame.sprite.Sprite):
    def __init__(self, sprite_name: str, speed: float = 1.0):
        super().__init__()
        self.sprite_name = sprite_name
        self.speed = speed
        self.image = pygame.image.load(f"assets/{sprite_name}.png")
        self.current_image = 0
        self.images = animation.get(sprite_name, [])

    # Méthode pour animer le sprite
    def animate(self):
        self.current_image += self.speed
        if self.current_image >= len(self.images):
            self.current_image = 0
        self.image = self.images[int(self.current_image)]

    def Update(self, sprite_name: str, speed: float):
        # Utilisez self.sprite_name et self.speed directement
        self.sprite_name = sprite_name
        self.speed = speed
        self.images = animation.get(self.sprite_name)
        self.animate()


# Fonction pour charger les images d'un sprite

def load_animation_images(dos_name: str, sprite_name: str, number_img: int):
    images = []
    path = os.path.join('assets', dos_name)
    for num in range(1, number_img):
        image_path = f'{path}/{sprite_name}{num}.png'
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
