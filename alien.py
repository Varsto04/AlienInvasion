import random
import pygame
from pygame.sprite import Sprite
from settings import Settings


class Alien(Sprite):
    def __init__(self, ai_game):
        pygame.sprite.Sprite.__init__(self)
        self.screen = ai_game.screen
        self.image = pygame.Surface((30, 40))
        self.images = ['images/alien.png', 'images/alien2.png', 'images/alien3.png']
        self.image = pygame.image.load(random.choice(self.images))
        self.rect = self.image.get_rect()
        self.settings = Settings()
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.rect.x = random.randrange(self.settings.screen_width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)

    def update(self):
        self.rect.x += self.settings.speedx
        self.rect.y += self.settings.speedy
        if self.rect.top > self.settings.screen_height + 10 or self.rect.left \
                < -25 or self.rect.right > self.settings.screen_width + 20:
            self.rect.x = random.randrange(self.settings.screen_width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
