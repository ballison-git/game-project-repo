import pygame
from pygame.sprite import Sprite

class Star(Sprite):
    #single star
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen

        #load star image
        self.image = pygame.image.load('star.bmp')
        self.rect = self.image.get_rect()

        #star each star near top left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #star position
        self.x = float(self.rect.x)