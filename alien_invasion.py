# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# Art from Kenney.nl
import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
import random
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from button2 import Button2
from explosion import Explosion
import pygame.font
from os import path
from pygame.sprite import Group


class AlienInvasion:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 1024)
        pygame.mixer.init()
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        background_images = ['images/cosmos.jpeg', 'images/cosmos2.jpeg', 'images/cosmos3.jpeg']
        self.background_image = pygame.image.load(random.choice(background_images))
        self.background_image = pygame.transform.scale(self.background_image,
                                                       (self.settings.screen_width, self.settings.screen_height))
        snd_dir = path.join(path.dirname(__file__), 'snd')
        self.shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
        self.expl_sounds = []
        for snd in ['expl3.wav', 'expl6.wav']:
            self.expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
        pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
        pygame.mixer.music.set_volume(0.7)
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.explosions = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_aliens()
        self.play_button = Button(self, "Play")
        self.stop_button = Button2(self, "Exit")

    def run_game(self):
        score = 0
        pygame.mixer.music.play(loops=-1)
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_explosions()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                mouse_pos2 = pygame.mouse.get_pos()
                self._check_stop_button(mouse_pos2)

    def _check_stop_button(self, mouse_pos2):
        button_clicked2 = self.stop_button.rect.collidepoint(mouse_pos2)
        if button_clicked2 and not self.stats.game_active:
            sys.exit()

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self.explosions.empty()
            self._create_aliens()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        self.shoot_sound.play()
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            self.stats.score += 1
            self.sb.prep_score()
            random.choice(self.expl_sounds).play()
        for collision in collisions:
            explosion = Explosion(collision.rect.center, 'lg')
            self.explosions.add(explosion)
            #explosion.update_explosion()
            alien = Alien(self)
            self.aliens.add(alien)

    def _create_aliens(self):
        for i in range(12):
            alien = Alien(self)
            self.aliens.add(alien)

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self.explosions.empty()
            self._create_aliens()
            #self.ship.center_ship()
            #sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_explosions(self):
        self.explosions.update()

    def _update_aliens(self):
        self.aliens.update()
        collisions = pygame.sprite.spritecollide(self.ship, self.aliens, False, pygame.sprite.collide_circle)
        if collisions:
            self._ship_hit()
            random.choice(self.expl_sounds).play()
        for collision in collisions:
            explosion = Explosion(collision.rect.center, 'lg')
            self.explosions.add(explosion)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.background_image, (0, 0))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.explosions.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()
        if not self.stats.game_active:
            self.stop_button.draw_button()
        pygame.display.flip()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
