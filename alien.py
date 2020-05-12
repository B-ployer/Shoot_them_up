import pygame
import random
from images import *
from bullet import *
from sprites import *
from sounds import *

pygame.init()

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = alien_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = -100
        self.speedx = 4
        self.speedy = 2
        self.lives = 20
        self.shoot_delay = 400
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > 0:
            self.rect.y = 0
            self.rect.x += self.speedx
            self.shoot()
            if self.rect.right > WIDTH or self.rect.left < 0:
                self.speedx = -self.speedx

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            alien_bullet = Bullet(self.rect.centerx, self.rect.bottom)
            all_sprites.add(alien_bullet)
            enemy_bullets.add(alien_bullet)
            shoot_sound.play()
