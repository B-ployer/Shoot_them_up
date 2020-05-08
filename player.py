import pygame
from sprites import all_sprites, bullets
from images import *
from parameters import *
from bullet import *
from sounds import *

pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)    для тестирования колайд-боксов
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        self.speedx = 0
        self.image = player_img
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
            self.image = player_img_left
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
            self.image = player_img_right
        if keystate[pygame.K_SPACE] and self.hidden == False:
            self.shoot()
        self.rect.x += self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        # показать, если скрыто
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        # тайм-аут для бонусов
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top, "player")
                all_sprites.add(bullet)
                bullets.add(bullet)
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery, "player")
                bullet2 = Bullet(self.rect.right, self.rect.centery, "player")
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
            shoot_sound.play()

    def hide(self):
        # временно скрыть игрока
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
