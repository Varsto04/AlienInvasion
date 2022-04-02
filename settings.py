import random


class Settings():
    def __init__(self):
        self.screen_width = 1920
        self.screen_height = 1000
        self.bg_color = (230, 230, 230)
        self.ship_speed = 5.5
        self.ship_limit = 3
        self.bullet_speed = 10
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0, 191, 255)
        self.alien_speed = 3.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        self.speedy = random.randrange(3, 5)
        self.speedx = random.randrange(-3, 3)
