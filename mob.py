import random
from parameters import *
from player import *
from images import *
from sprites import *

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_imges)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .9 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)    для тестирования колайд-боксов
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        time_to_arriving = 0.125 * (((player.rect.x - self.rect.x) ** 2) + (player.rect.y - self.rect.y) ** 2) ** 0.5
        # self.speedy = random.randrange(1, 8)     простой параметр скорости по Y
        # self.speedx = random.randrange(-3, 3)    простой параметр скорости по X
        self.speedx = (player.rect.x - self.rect.x) / time_to_arriving
        self.speedy = (player.rect.y - self.rect.y) / time_to_arriving
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
        if self.image_orig == meteor_imges[0]:
            self.lives = 4
        elif self.image_orig == meteor_imges[1] or self.image_orig == meteor_imges[2]:
            self.lives = 3
        elif self.image_orig == meteor_imges[4] or self.image_orig == meteor_imges[5]:
            self.lives = 2
        else:
            self.lives = 1

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 25 or self.rect.left > WIDTH + 25 or self.rect.right < 0:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 8)

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
