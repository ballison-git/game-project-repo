import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    # class that manages bullets fired from a ship

    def __init__(self, ai_game):
        #create a bullet object at ships current position
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #create bullet rect at (0,0) then correct position
        self.rect = pygame.Rect(0,0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        #store bullets position as a decimal value
        self.y = float(self.rect.y)

    def update(self):
        #update movement of the bullet
        self.y -= self.settings.bullet_speed
        #update rect position
        self.rect.y = self.y

    def draw_bullet(self):
        #draw bullet to the screen
        pygame.draw.rect(self.screen, self.color, self.rect)